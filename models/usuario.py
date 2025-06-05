# models/usuario.py
from typing import List, Optional, TYPE_CHECKING
from models.livro import Livro
from utils.helpers import limpar_tela, voltando, exibir_mensagem_e_aguardar, sair_da_conta_mensagem, texto_placeholder_livro

if TYPE_CHECKING:
    from repositories.repositorio_usuarios import RepositorioUsuarios
    from repositories.repositorio_livros import RepositorioLivros

class Usuario:
    def __init__(self, nome: str, repo_usuarios: 'RepositorioUsuarios', repo_livros: 'RepositorioLivros'):
        self.nome = nome
        self.repo_usuarios = repo_usuarios
        self.repo_livros = repo_livros
        # A biblioteca pessoal é carregada sob demanda ou através de um método específico

    def _carregar_biblioteca_pessoal(self) -> List[Livro]:
        return self.repo_usuarios.obter_biblioteca_usuario(self.nome)

    def _salvar_alteracoes_conta(self, novo_nome: Optional[str] = None, nova_senha: Optional[str] = None) -> bool:
        nome_antigo = self.nome
        sucesso, msg = self.repo_usuarios.alterar_dados_usuario(nome_antigo, novo_nome, nova_senha)
        if sucesso and novo_nome:
            self.nome = novo_nome
        exibir_mensagem_e_aguardar(msg)
        return sucesso

    def _menu_adicionar_livros_biblioteca(self):
        limpar_tela()
        print("=== Adicionar Livros à sua Biblioteca ===")
        
        biblioteca_pessoal_atual = self._carregar_biblioteca_pessoal()
        titulos_na_biblioteca = {livro.titulo for livro in biblioteca_pessoal_atual}
        
        livros_disponiveis_catalogo = self.repo_livros.listar_todos()
        livros_para_adicionar = [
            livro for livro in livros_disponiveis_catalogo if livro.titulo not in titulos_na_biblioteca
        ]

        if not livros_para_adicionar:
            exibir_mensagem_e_aguardar("Nenhum livro novo para adicionar ou todos os livros do catálogo já estão na sua biblioteca.")
            return

        print("\nLivros disponíveis para adicionar:")
        for i, livro in enumerate(livros_para_adicionar, 1):
            print(f"{i}. {livro.titulo} - {livro.genero}")
        
        print("0. Voltar")

        while True:
            escolha = input("\nDigite o número do livro para adicionar (ou 0 para voltar): ").strip()
            if not escolha.isdigit():
                print("Entrada inválida. Por favor, digite um número.")
                continue
            
            idx_escolha = int(escolha)
            if idx_escolha == 0:
                break
            
            if 1 <= idx_escolha <= len(livros_para_adicionar):
                livro_escolhido = livros_para_adicionar[idx_escolha - 1]
                if self.repo_usuarios.adicionar_livro_na_biblioteca_usuario(self.nome, livro_escolhido):
                    exibir_mensagem_e_aguardar(f"Livro '{livro_escolhido.titulo}' adicionado com sucesso!", limpar_apos=False)
                else:
                    # Isso pode acontecer se houver uma condição de corrida ou erro inesperado
                    exibir_mensagem_e_aguardar(f"Não foi possível adicionar o livro '{livro_escolhido.titulo}'.", limpar_apos=False)
                self._menu_adicionar_livros_biblioteca() # Recarrega o menu
                return # Sai da função atual para evitar loops aninhados de input
            else:
                print("Opção inválida. Tente novamente.")
        voltando()


    def _menu_gerenciar_minha_biblioteca(self):
        while True:
            limpar_tela()
            print(f"=== Minha Biblioteca - {self.nome} ===")
            biblioteca_pessoal = self._carregar_biblioteca_pessoal()

            if not biblioteca_pessoal:
                print("Sua biblioteca está vazia.")
            else:
                for i, livro in enumerate(biblioteca_pessoal, 1):
                    print(f"{i}. {livro.titulo} - {livro.genero}")
            
            print("\nOpções:")
            print("1. Ler livro selecionado")
            print("2. Remover livro selecionado")
            print("0. Voltar ao menu principal")

            escolha_acao = input("\nEscolha uma opção: ").strip()

            if escolha_acao == "0":
                voltando()
                break
            
            if not biblioteca_pessoal and escolha_acao in ["1", "2"]:
                exibir_mensagem_e_aguardar("Sua biblioteca está vazia. Não há livros para selecionar.")
                continue

            if escolha_acao in ["1", "2"]:
                num_livro_str = input("Digite o número do livro: ").strip()
                if not num_livro_str.isdigit():
                    exibir_mensagem_e_aguardar("Entrada inválida. Deve ser um número.")
                    continue
                
                idx_livro = int(num_livro_str) -1

                if 0 <= idx_livro < len(biblioteca_pessoal):
                    livro_selecionado = biblioteca_pessoal[idx_livro]
                    if escolha_acao == "1":
                        limpar_tela()
                        print(f"{livro_selecionado.titulo}...\n")
                        texto_placeholder_livro() # Simula a leitura
                        voltando()
                    
                    elif escolha_acao == "2":
                        confirmacao = input(f"Tem certeza que deseja remover '{livro_selecionado.titulo}' da sua biblioteca? (s/n): ").strip().lower()
                        if confirmacao == 's':
                            removido = self.repo_usuarios.remover_livro_da_biblioteca_usuario(self.nome, livro_selecionado.titulo)
                            if removido:
                                exibir_mensagem_e_aguardar(f"Livro '{removido.titulo}' removido com sucesso.")
                            else:
                                exibir_mensagem_e_aguardar(f"Não foi possível remover o livro.") # Deveria ser raro
                        else:
                            exibir_mensagem_e_aguardar("Remoção cancelada.")
                else:
                    exibir_mensagem_e_aguardar("Número do livro inválido.")
            else:
                exibir_mensagem_e_aguardar("Opção inválida.")


    def _menu_alterar_conta(self):
        while True:
            limpar_tela()
            print(f"=== Alterar Conta - {self.nome} ===")
            print("1. Alterar nome de usuário")
            print("2. Alterar senha")
            print("3. Excluir minha conta")
            print("0. Voltar")
            
            escolha = input("\nEscolha uma opção: ").strip()
            novo_nome_usuario = None
            nova_senha_usuario = None

            if escolha == "0":
                voltando()
                break
            elif escolha == "1":
                novo_nome_usuario = input("Digite o novo nome de usuário: ").strip()
                if not novo_nome_usuario:
                    exibir_mensagem_e_aguardar("Nome de usuário não pode ser vazio.")
                    continue
                if novo_nome_usuario == self.nome:
                    exibir_mensagem_e_aguardar("O novo nome de usuário é igual ao atual.")
                    continue
                # A senha atual não é pedida para alterar o nome, mas poderia ser um requisito de segurança
                self._salvar_alteracoes_conta(novo_nome=novo_nome_usuario)

            elif escolha == "2":
                from getpass import getpass
                senha_atual = getpass("Digite sua senha atual para confirmar: ").strip()
                senha_correta = self.repo_usuarios.buscar_senha(self.nome)
                if senha_atual != senha_correta:
                    exibir_mensagem_e_aguardar("Senha atual incorreta.")
                    continue
                
                nova_senha_usuario = getpass("Digite a nova senha: ").strip()
                if not nova_senha_usuario:
                    exibir_mensagem_e_aguardar("Nova senha não pode ser vazia.")
                    continue
                conf_nova_senha = getpass("Confirme a nova senha: ").strip()
                if nova_senha_usuario != conf_nova_senha:
                    exibir_mensagem_e_aguardar("As novas senhas não coincidem.")
                    continue
                self._salvar_alteracoes_conta(nova_senha=nova_senha_usuario)
            
            elif escolha == "3":
                from getpass import getpass
                print("\nATENÇÃO: Esta ação é irreversível e todos os seus dados serão perdidos.")
                conf_nome = input(f"Digite seu nome de usuário '{self.nome}' para confirmar: ").strip()
                conf_senha = getpass("Digite sua senha para confirmar: ").strip()

                senha_correta = self.repo_usuarios.buscar_senha(self.nome)

                if conf_nome == self.nome and conf_senha == senha_correta:
                    certeza = input("Você tem CERTEZA ABSOLUTA que deseja excluir sua conta? (sim/não): ").strip().lower()
                    if certeza == "sim":
                        if self.repo_usuarios.remover_usuario(self.nome):
                            exibir_mensagem_e_aguardar("Conta excluída com sucesso. Você será desconectado.", segundos_espera=3)
                            return True # Sinaliza que a conta foi excluída e o loop principal deve sair
                        else:
                            exibir_mensagem_e_aguardar("Erro ao excluir a conta.")
                    else:
                        exibir_mensagem_e_aguardar("Exclusão cancelada.")
                else:
                    exibir_mensagem_e_aguardar("Nome de usuário ou senha incorretos. Exclusão cancelada.")
            else:
                exibir_mensagem_e_aguardar("Opção inválida.")
        return False # Sinaliza para continuar no menu


    def menu_principal_usuario(self) -> bool: # Retorna True se o usuário quiser deslogar/conta excluída
        # Menu principal para o usuário logado.
        limpar_tela()
        while True:
            print(f"\nOlá {self.nome}, seja bem-vindo(a)!")
            print("Escolha o que fazer:")
            print("1. Adicionar livros à sua biblioteca")
            print("2. Gerenciar sua biblioteca")
            print("3. Alterar dados da sua conta")
            print("4. Sair da conta")
            print(35*"-=")
            
            escolha = input("Opção: ").strip()
            limpar_tela()

            if escolha == "1":
                self._menu_adicionar_livros_biblioteca()
            elif escolha == "2":
                self._menu_gerenciar_minha_biblioteca()
            elif escolha == "3":
                conta_excluida = self._menu_alterar_conta()
                if conta_excluida:
                    return True # Deslogar
            elif escolha == "4":
                sair_da_conta_mensagem()
                return True # Deslogar
            else:
                exibir_mensagem_e_aguardar("Opção inválida, tente novamente.")
            
            if self.nome not in self.repo_usuarios.listar_todos_nomes_usuarios(): # Verifica se o usuário ainda existe (pode ter sido excluído)
                return True # Força logout se o usuário não existe mais