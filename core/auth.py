import os
import json
from core.defs import voltando, saindo, carregar_usuarios, salvar_usuarios
from getpass import getpass

CAMINHO_DB = "db/usuarios.json"

# Garante que existe ao menos o admin
if not os.path.exists("db"):
    os.makedirs("db")

if not os.path.exists(CAMINHO_DB):
    with open(CAMINHO_DB, "w", encoding="utf-8") as f:
        json.dump({"admin": {"senha": "admin", "biblioteca": []}}, f, indent=4)

def login_ou_cadastro():
    while True:
        os.system('cls')
        print("1) Login")
        print("2) Cadastro")
        print("0) Sair")
        escolha = input("\nEscolha: ")

        usuarios = carregar_usuarios()

        if escolha == "1":
            usuario = input("Usuário: ").strip()
            senha = getpass("Senha: ").strip()
            if usuario in usuarios and usuarios[usuario]["senha"] == senha:
                print("Login bem-sucedido!")
                voltando()
                return usuario, usuarios
            else:
                print("Usuário ou senha incorretos.")
                input("Pressione qualquer tecla para tentar novamente.")
                continue

        elif escolha == "2":
            usuario = input("Digite o nome de usuário desejado: ").strip()
            if usuario in usuarios:
                print("Usuário já existe.")
                input("Pressione qualquer tecla para tentar novamente.")
                continue
            senha = getpass("Digite a senha: ").strip()
            senha_confirm = getpass("Confirme a senha: ").strip()
            if senha != senha_confirm:
                print("As senhas não coincidem.")
                input("Pressione qualquer tecla para tentar novamente.")
                continue
            usuarios[usuario] = {"senha": senha, "biblioteca": []}
            salvar_usuarios(usuarios)
            print("Cadastro realizado com sucesso!")
            voltando()
            return usuario, usuarios

        elif escolha == "0":
            saindo()
            exit()

        else:
            print("Escolha inválida.")
            input("Pressione qualquer tecla para continuar.")
