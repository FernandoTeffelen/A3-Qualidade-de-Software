import os
import time

from core.auth import login_ou_cadastro, carregar_usuarios, salvar_usuarios
from core.defs import livros_por_genero, menu_usuario, salvar_dados, menu_admin

def iniciar_programa():
    dados = carregar_usuarios()
    usuarios = dados.get('usuarios', [])
    senhas = dados.get('senhas', {})
    bibliotecas = dados.get('bibliotecas', {})

    while True:
        while True:
            acao = input("Digite 'login' para entrar ou 'cadastro' para criar conta: ").strip().lower()

            if acao == 'login':
                usuario = input("Usuário: ").strip()
                senha = input("Senha: ").strip()

                if usuario in usuarios and senhas.get(usuario) == senha:
                    print(f"Bem-vindo, {usuario}!")
                    if usuario == 'admin':
                        # chama função menu_admin() ou o que for para admin
                        menu_admin()
                    else:
                        # chama função menu_usuario(usuario) ou fluxo do usuário normal
                        menu_usuario(usuario)
                    break
                else:
                    print("Usuário ou senha incorretos.")

            elif acao == 'cadastro':
                usuario = input("Escolha um nome de usuário: ").strip()
                if usuario in usuarios:
                    print("Usuário já existe.")
                    continue
                senha = input("Escolha uma senha: ").strip()
                usuarios.append(usuario)
                senhas[usuario] = senha
                bibliotecas[usuario] = []

                dados = {
                    'usuarios': usuarios,
                    'senhas': senhas,
                    'bibliotecas': bibliotecas
                }
                salvar_usuarios(dados)
                print("Cadastro realizado com sucesso!")
            else:
                print("Opção inválida.")





def carregar_dados():
    import json
    global usuarios, senhas, bibliotecas, livros, generos

    if os.path.exists("dados.json"):
        with open("dados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            usuarios = list(dados.get("usuarios", []))
            senhas = list(dados.get("senhas", []))
            bibliotecas = dados.get("bibliotecas", {})
            livros = dados.get("livros", [])
            generos = dados.get("generos", [])
    else:
        usuarios = []
        senhas = []
        bibliotecas = {}
        livros = []
        generos = []
    return usuarios, senhas, bibliotecas, livros, generos

def main():
    os.system('cls')
    usuarios, senhas, bibliotecas, livros, generos = carregar_dados()

    while True:
        usuario, usuarios_dict = login_ou_cadastro()

        # Sincroniza dados do JSON para memória
        bibliotecas = {u: d.get("biblioteca", []) if isinstance(d, dict) else [] for u, d in usuarios_dict.items()}
        # Atualiza dados globais
        from core.defs import usuarios as g_usuarios, senhas as g_senhas, bibliotecas as g_bibliotecas, livros as g_livros, generos as g_generos
        g_usuarios.clear()
        g_usuarios.extend(usuarios_dict.keys())
        g_senhas.clear()
        g_senhas.extend([usuarios_dict[u]["senha"] for u in usuarios_dict])
        g_bibliotecas.clear()
        g_bibliotecas.update(bibliotecas)

        # Atualiza livros e gêneros
        # Se preferir carregar de db.py, chame funções específicas para carregar livros/gêneros

        menu_usuario(usuario)

        # Após sair do menu do usuário, salva as alterações
        salvar_usuarios({u: {"senha": usuarios_dict[u]["senha"], "biblioteca": g_bibliotecas.get(u, [])} for u in usuarios_dict})
        salvar_dados()

if __name__ == "__main__":
    main()
