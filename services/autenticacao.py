# services/autenticacao.py
from getpass import getpass # Para esconder a senha
from typing import Optional
from repositories.repositorio_usuarios import RepositorioUsuarios

class ServicoAutenticacao:
    def __init__(self, repo_usuarios: RepositorioUsuarios):
        self.repo_usuarios = repo_usuarios

    def login(self) -> Optional[str]:
        # Solicita usuário e senha e tenta autenticar.
        usuario_input = input("Usuário: ").strip()
        senha_input = getpass("Senha: ").strip() # getpass esconde a senha

        senha_armazenada = self.repo_usuarios.buscar_senha(usuario_input)

        if senha_armazenada and senha_armazenada == senha_input:
            return usuario_input
        else:
            print("Usuário ou senha incorretos.")
            return None

    def cadastro(self) -> Optional[str]:
        # Solicita dados para cadastro de um novo usuário.
        usuario_input = input("Escolha um nome de usuário: ").strip()
        if not usuario_input:
            print("Nome de usuário não pode ser vazio.")
            return None
        
        if self.repo_usuarios.existe_usuario(usuario_input):
            print("Usuário já existe.")
            return None
        
        print("\nATENÇÃO: Sua senha ficara oculta para sua segurança.")
        senha_input = getpass("Escolha uma senha: ").strip()
        if not senha_input:
            print("Senha não pode ser vazia.")
            return None
            
        senha_confirmacao = getpass("Confirme a senha: ").strip()

        if senha_input != senha_confirmacao:
            print("As senhas não coincidem.")
            return None

        if self.repo_usuarios.adicionar_usuario(usuario_input, senha_input):
            print("Cadastro realizado com sucesso!")
            return usuario_input
        else:
            # Esta mensagem não deveria aparecer se as verificações acima funcionarem
            print("Falha ao cadastrar. Tente novamente.") 
            return None