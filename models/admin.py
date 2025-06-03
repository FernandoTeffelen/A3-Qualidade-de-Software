# models/admin.py
from typing import TYPE_CHECKING, List, Optional
from models.livro import Livro
from utils.helpers import limpar_tela, aguardar_e_limpar, exibir_mensagem_e_aguardar, sair_da_conta_mensagem, texto_placeholder_livro

if TYPE_CHECKING:
    from repositories.repositorio_usuarios import RepositorioUsuarios
    from repositories.repositorio_livros import RepositorioLivros

class Admin:
    def __init__(self, nome: str, repo_usuarios: 'RepositorioUsuarios', repo_livros: 'RepositorioLivros'):
        self.nome = nome
        self.repo_usuarios = repo_usuarios
        self.repo_livros = repo_livros

    def _menu_cadastro_novo_livro(self):
        limpar_tela()
        print("=== Cadastro de Novo Livro ===")
        while True:
            titulo = input("Título do livro (ou 'voltar' para sair): ").strip()
            if titulo.lower() == 'voltar':
                break
            if not titulo:
                print("Título não pode ser vazio.")
                continue

            genero = input("Gênero do livro: ").strip()
            if not genero:
                print("Gênero não pode ser vazio.")
                continue

            if self.repo_livros.adicionar_livro(titulo, genero):
                exibir_mensagem_e_aguardar(f"Livro '{titulo}' cadastrado com sucesso!", limpar_apos=False)
            else:
                exibir_mensagem_e_aguardar(f"Livro '{titulo}' já existe no catálogo.", limpar_apos=False)
            
            continuar = input("Deseja cadastrar outro livro? (s/n): ").strip().lower()
            if continuar != 's':
                break
            limpar_tela()
        aguardar_e_limpar()

    def _menu_alterar_livro_catalogo(self):
        limpar_tela()
        print("=== Alterar Livro do Catálogo ===")
        livros_catalogo: List[Livro] = self.repo_livros.listar_todos()
        if not livros_catalogo:
            exibir_mensagem_e_aguardar("Nenhum livro cadastrado no catálogo para alterar.")
            return

        for i, livro in enumerate(livros_catalogo, 1):
            print(f"{i}. {livro.titulo} - {livro.genero}")
        
        try:
            pos_str = input("\nDigite o número do livro que deseja alterar (ou qualquer letra para voltar): ").strip()
            if not pos_str.isdigit():
                aguardar_e_limpar()
                return
                
            posicao = int(pos_str) - 1
            if 0 <= posicao < len(livros_catalogo):
                livro_original = livros_catalogo[posicao]
                print(f"\nAlterando livro: {livro_original.titulo}")
                
                novo_titulo = input(f"Novo título (atual: {livro_original.titulo}): ").strip()
                if not novo_titulo: novo_titulo = livro_original.titulo # Mantém o original se vazio

                novo_genero = input(f"Novo gênero (atual: {livro_original.genero}): ").strip()
                if not novo_genero: novo_genero = livro_original.genero # Mantém o original se vazio

                if self.repo_livros.atualizar_livro(livro_original.titulo, novo_titulo, novo_genero):
                    exibir_mensagem_e_aguardar(f"Livro '{novo_titulo}' atualizado com sucesso!")
                else:
                    # Mensagem de erro específica já é mostrada pelo repositório se o título novo já existe
                    exibir_mensagem_e_aguardar(f"Não foi possível atualizar o livro.")
            else:
                exibir_mensagem_e_aguardar("Posição inválida.")
        except ValueError:
            exibir_mensagem_e_aguardar("Entrada inválida.")
        aguardar_e_limpar(segundos=0.1) # Pequeno delay para a msg do input ser vista se for o caso

    def _menu_gerenciar_livros_cadastrados(self):
        while True:
            limpar_tela()
            print("=== Livros Cadastrados no Catálogo ===")
            livros_catalogo: List[Livro] = self.repo_livros.listar_todos()
            if not livros_catalogo:
                print("Nenhum livro cadastrado.")
            else:
                for i, livro in enumerate(livros_catalogo, 1):
                    print(f"{i}. {livro.titulo} - {livro.genero}")
            
            print("\nOpções:")
            print("1. Excluir livro selecionado")
            print("2. Visualizar conteúdo do livro selecionado (simulação)")
            print("0. Voltar")
            
            escolha_acao = input("\nEscolha uma opção: ").strip()

            if escolha_acao == "0":
                aguardar_e_limpar()
                break
            
            if not livros_catalogo and escolha_acao in ["1", "2"]:
                exibir_mensagem_e_aguardar("Nenhum livro para selecionar.")
                continue

            if escolha_acao in ["1", "2"]:
                num_livro_str = input("Digite o número do livro: ").strip()
                if not num_livro_str.isdigit():
                    exibir_mensagem_e_aguardar("Entrada inválida. Deve ser um número.")
                    continue
                
                idx_livro = int(num_livro_str) -1

                if 0 <= idx_livro < len(livros_catalogo):
                    livro_selecionado = livros_catalogo[idx_livro]
                    
                    if escolha_acao == "1":
                        confirmacao = input(f"Tem certeza que deseja excluir '{livro_selecionado.titulo}' do catálogo? (s/n): ").strip().lower()
                        if confirmacao == 's':
                            removido = self.repo_livros.remover_livro_por_titulo(livro_selecionado.titulo)
                            if removido:
                                exibir_mensagem_e_aguardar(f"Livro '{removido.titulo}' excluído do catálogo.")
                            else:
                                exibir_mensagem_e_aguardar("Não foi possível excluir o livro.")
                        else:
                            exibir_mensagem_e_aguardar("Exclusão cancelada.")
                    
                    elif escolha_acao == "2":
                        limpar_tela()
                        print(f"Visualizando '{livro_selecionado.titulo}'...\n")
                        texto_placeholder_livro() 
                else:
                    exibir_mensagem_e_aguardar("Número do livro inválido.")
            else:
                exibir_mensagem_e_aguardar("Opção inválida.")


    def _menu_gerenciar_usuarios_cadastrados(self):
        while True:
            limpar_tela()
            print("=== Usuários Cadastrados ===")
            nomes_usuarios: List[str] = self.repo_usuarios.listar_todos_nomes_usuarios(incluir_admin=False) 

            if not nomes_usuarios:
                print("Nenhum usuário cadastrado.")
            else:
                for i, nome_usr in enumerate(nomes_usuarios, 1):
                    print(f"{i}. {nome_usr}")
            
            print("\nOpções:")
            print("1. Excluir usuário selecionado")
            print("2. Visualizar biblioteca do usuário selecionado")
            print("0. Voltar")

            escolha_acao = input("\nEscolha uma opção: ").strip()
            if escolha_acao == "0":
                aguardar_e_limpar()
                break

            if not nomes_usuarios and escolha_acao in ["1", "2"]:
                exibir_mensagem_e_aguardar("Nenhum usuário para gerenciar.")
                continue
            
            if escolha_acao in ["1", "2"]:
                num_usr_str = input("Digite o número do usuário: ").strip()
                if not num_usr_str.isdigit():
                    exibir_mensagem_e_aguardar("Entrada inválida. Deve ser um número.")
                    continue
                idx_usr = int(num_usr_str) - 1

                if 0 <= idx_usr < len(nomes_usuarios):
                    usuario_selecionado_nome = nomes_usuarios[idx_usr]
                    if escolha_acao == "1":
                        confirmacao = input(f"Tem certeza que deseja excluir o usuário '{usuario_selecionado_nome}'? \nEsta ação é irreversível e o usuário perderá sua biblioteca! (s/n): ").strip().lower()
                        if confirmacao == 's':
                            if self.repo_usuarios.remover_usuario(usuario_selecionado_nome):
                                exibir_mensagem_e_aguardar(f"Usuário '{usuario_selecionado_nome}' removido com sucesso.")
                            else:
                                exibir_mensagem_e_aguardar(f"Não foi possível remover o usuário '{usuario_selecionado_nome}'.")
                        else:
                            exibir_mensagem_e_aguardar("Exclusão cancelada.")
                    
                    elif escolha_acao == "2":
                        limpar_tela()
                        print(f"--- Biblioteca de {usuario_selecionado_nome} ---")
                        biblioteca_usr: List[Livro] = self.repo_usuarios.obter_biblioteca_usuario(usuario_selecionado_nome)
                        if not biblioteca_usr:
                            print("Este usuário não possui livros em sua biblioteca.")
                        else:
                            for i, livro_usr in enumerate(biblioteca_usr, 1):
                                print(f"{i}. {livro_usr.titulo} - {livro_usr.genero}")
                        input("\nPressione qualquer tecla para voltar ao menu de usuários...")
                        aguardar_e_limpar(segundos=0.1)
                else:
                    exibir_mensagem_e_aguardar("Número do usuário inválido.")
            else:
                exibir_mensagem_e_aguardar("Opção inválida.")


    def menu_principal_admin(self) -> bool: 
        # Menu principal para o administrador logado.
        limpar_tela()
        while True:
            print(f"\n=== PAINEL DO ADMINISTRADOR ({self.nome}) ===")
            print("1. Cadastrar novo livro no catálogo")
            print("2. Alterar dados de um livro do catálogo")
            print("3. Gerenciar livros cadastrados (ver/excluir)")
            print("4. Gerenciar usuários cadastrados (ver biblioteca/excluir)")
            print("5. Sair da conta")
            print(35*"-=")

            escolha = input("Opção: ").strip()

            if escolha == "1":
                limpar_tela()
                self._menu_cadastro_novo_livro()
            elif escolha == "2":
                limpar_tela()
                self._menu_alterar_livro_catalogo()
            elif escolha == "3":
                limpar_tela()
                self._menu_gerenciar_livros_cadastrados()
            elif escolha == "4":
                limpar_tela()
                self._menu_gerenciar_usuarios_cadastrados()
            elif escolha == "5":
                limpar_tela()
                sair_da_conta_mensagem()
                return True # Deslogar
            else:
                exibir_mensagem_e_aguardar("Opção inválida, tente novamente.")