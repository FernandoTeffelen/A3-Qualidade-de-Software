# models/sistema.py
from typing import Optional

from repositories.repositorio_livros import RepositorioLivros
from repositories.repositorio_usuarios import RepositorioUsuarios
from services.autenticacao import ServicoAutenticacao
from models.usuario import Usuario
from models.admin import Admin
from utils.helpers import limpar_tela, aguardar_e_limpar, exibir_mensagem_e_aguardar

class Sistema:
    def __init__(self):
        self.repo_livros = RepositorioLivros()
        self.repo_usuarios = RepositorioUsuarios()
        self.servico_auth = ServicoAutenticacao(self.repo_usuarios)
        self.usuario_logado: Optional[Usuario | Admin] = None # Python 3.10+ para |

    def iniciar_sessao(self):
        # Tenta logar ou cadastrar um usuário e direciona para o menu apropriado.
        limpar_tela()
        while True: 
            if self.usuario_logado: # Se já estiver logado (raro cair aqui, mas por segurança)
                self._direcionar_para_menu()
                if not self.usuario_logado: # Se fez logout
                    continue # Volta para o menu de login/cadastro

            print("Bem-vindo à Biblioteca Virtual!")
            print("1. Login")
            print("2. Cadastro")
            print("0. Sair do Programa")
            acao = input("Escolha uma opção: ").strip().lower()
            limpar_tela()

            nome_usuario_sessao = None
            if acao == '1':
                nome_usuario_sessao = self.servico_auth.login()
                if nome_usuario_sessao:
                    if nome_usuario_sessao == "admin":
                        self.usuario_logado = Admin(nome_usuario_sessao, self.repo_usuarios, self.repo_livros)
                    else:
                        self.usuario_logado = Usuario(nome_usuario_sessao, self.repo_usuarios, self.repo_livros)
                    exibir_mensagem_e_aguardar(f"Login bem-sucedido! Bem-vindo(a), {nome_usuario_sessao}!", segundos_espera=1.5)
                else:
                    exibir_mensagem_e_aguardar("Falha no login. Tente novamente.", segundos_espera=1.5)
            
            elif acao == '2':
                nome_usuario_sessao = self.servico_auth.cadastro()
                if nome_usuario_sessao: # Cadastro bem-sucedido, loga automaticamente
                    self.usuario_logado = Usuario(nome_usuario_sessao, self.repo_usuarios, self.repo_livros)
                    exibir_mensagem_e_aguardar(f"Cadastro realizado! Bem-vindo(a), {nome_usuario_sessao}!", segundos_espera=1.5)
                else:
                    exibir_mensagem_e_aguardar("Falha no cadastro. Verifique os dados e tente novamente.", segundos_espera=1.5)

            elif acao == '0':
                print("Saindo do programa...")
                aguardar_e_limpar(1)
                break # Encerra o loop de login/cadastro e o programa
            
            else:
                exibir_mensagem_e_aguardar("Opção inválida.", segundos_espera=1.5)

            if self.usuario_logado:
                self._direcionar_para_menu()


    def _direcionar_para_menu(self):
        # Direciona para o menu do admin ou do usuário comum.
        if not self.usuario_logado:
            return

        deslogar = False
        if isinstance(self.usuario_logado, Admin):
            deslogar = self.usuario_logado.menu_principal_admin()
        elif isinstance(self.usuario_logado, Usuario):
            deslogar = self.usuario_logado.menu_principal_usuario()
        
        if deslogar:
            self.usuario_logado = None # Efetua o logout
            limpar_tela()
            print("Você foi desconectado.")
            aguardar_e_limpar(1.5)