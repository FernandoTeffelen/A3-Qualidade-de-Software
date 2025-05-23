import os
import time

from core.auth import login_ou_cadastro, carregar_usuarios, salvar_usuarios
from core.defs import livros_por_genero, menu_usuario, salvar_dados, menu_admin
from models.sistema import Sistema

def iniciar_programa():
    sistema = Sistema()

    while True:
        while True:
            acao = input("Digite 'login' para entrar ou 'cadastro' para criar conta: ").strip().lower()

            if acao == 'login':
                usuario = input("Usuário: ").strip()
                senha = input("Senha: ").strip()
                usuario_logado = sistema.login(usuario, senha)
                if usuario_logado:
                    print(f"Bem-vindo, {usuario_logado.nome}!")
                    if usuario_logado.nome == 'admin':
                        menu_admin()
                    else:
                        menu_usuario(usuario_logado.nome)
                    break
                else:
                    print("Usuário ou senha incorretos.")

            elif acao == 'cadastro':
                usuario = input("Escolha um nome de usuário: ").strip()
                senha = input("Escolha uma senha: ").strip()
                sucesso, msg = sistema.cadastro(usuario, senha)
                print(msg)
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
