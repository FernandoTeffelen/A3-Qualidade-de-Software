# services/autenticacao.py
from getpass import getpass # Para esconder a senha
from typing import Optional # ADICIONADO: Importar Optional
from repositories.repositorio_usuarios import RepositorioUsuarios
# Futuramente, importaria as classes Usuario e Admin de models
# from models.usuario import Usuario
# from models.admin import Admin

class ServicoAutenticacao:
    def __init__(self, repo_usuarios: RepositorioUsuarios):
        self.repo_usuarios = repo_usuarios

    def login(self) -> Optional[str]: # Retorna o nome do usuário logado ou None
        """ Solicita usuário e senha e tenta autenticar. """
        usuario_input = input("Usuário: ").strip()
        senha_input = getpass("Senha: ").strip() # getpass esconde a senha

        senha_armazenada = self.repo_usuarios.buscar_senha(usuario_input)

        if senha_armazenada and senha_armazenada == senha_input:
            return usuario_input # Retorna o nome do usuário para ser usado depois
        else:
            print("Usuário ou senha incorretos.")
            return None

    def cadastro(self) -> Optional[str]: # Retorna o nome do usuário cadastrado ou None
        """ Solicita dados para cadastro de um novo usuário. """
        usuario_input = input("Escolha um nome de usuário: ").strip()
        if not usuario_input:
            print("Nome de usuário não pode ser vazio.")
            return None
        
        if self.repo_usuarios.existe_usuario(usuario_input):
            print("Usuário já existe.")
            return None
        
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