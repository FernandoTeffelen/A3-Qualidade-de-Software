import os
from models.usuario import Usuario
from models.biblioteca import Biblioteca

class Sistema:
    def __init__(self):
        self.biblioteca = Biblioteca()
        self.usuario_logado = None

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def iniciar(self):
        while True:
            opcao = input("Você já possui cadastro? \n1) sim \n2) não\n")
            self.limpar_tela()

            if opcao == '1':
                self.login()
                break
            elif opcao == '2':
                self.cadastro()
                break
            else:
                print("Digite uma das duas opções, 1 ou 2.")

    def login(self):
        print("Entrar na conta\n" + "-"*40)
        nome = input("Usuário: ")
        senha = input("Senha: ")
        if self.biblioteca.autenticar(nome, senha):
            self.usuario_logado = Usuario(nome, senha)
            print(f"Bem-vindo, {nome}!")
        else:
            print("Usuário ou senha inválidos.")
            self.login()

    def cadastro(self):
        print("Vamos fazer seu cadastro\n" + "-"*40)
        while True:
            nome = input("Digite seu nome de usuário: ")
            senha = input("Escolha sua senha: ")

            if self.biblioteca.usuario_existe(nome):
                self.limpar_tela()
                print("Usuário já utilizado, tente outro!")
            elif nome == '':
                self.limpar_tela()
                print("Seu usuário deve conter ao menos 1 caractere")
            elif len(senha) < 6:
                self.limpar_tela()
                print("Sua senha deve conter ao menos 6 caracteres")
            else:
                self.biblioteca.cadastrar_usuario(nome, senha)
                self.usuario_logado = Usuario(nome, senha)
                self.limpar_tela()
                print("Cadastro realizado com sucesso!")
                break
