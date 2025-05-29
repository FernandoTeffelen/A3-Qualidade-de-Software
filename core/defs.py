import os
import time
import json

from core.db import livros, generos, usuarios, senhas, bibliotecas

CAMINHO_USUARIOS = "db/usuarios.json"
CAMINHO_LIVROS = "db/livros.json"

def voltando():
    time.sleep(1)
    os.system('cls')

def saindo():
    print("Saindo da conta...")

def mostrar_livros():
    print("\nLivros cadastrados:")
    for i, livro in enumerate(livros, start=1):
        print(f"{i}. {livro['titulo']} - {livro['genero']}")

def mostrar_usuarios():
    print("Usuários cadastrados:")
    for i, usuario in enumerate(usuarios):
        print(f"{i} - {usuario}")

def texto():
    print("Texto do livro...")

def adicionar_livro(usuario, posicao):
    bibliotecas[usuario].append(livros[posicao])

def livros_por_genero(genero_escolhido):
    return [i for i, g in enumerate(generos) if g == genero_escolhido]

def cadastro_novo_livro():
    os.system('cls')
    print("Cadastro de um novo livro.\nOu digite \"voltar\", para voltar ao menu.\n")
    print(20*"-=")
    global livros  # para usar a lista global carregada do JSON
    while True:
        titulo = input("Nome do livro: ")
        if titulo.lower() == 'voltar':
            voltando()
            break
        genero = input("Gênero do livro: ")
        
        # Adiciona novo livro na lista em memória
        livros.append({"titulo": titulo, "genero": genero})
        
        # Salva a lista atualizada no arquivo JSON
        salvar_livros(livros)

        os.system('cls')
        while True:
            continuar = input("Deseja cadastrar outro livro? \n1) sim \n2) não\n")
            print(20*"-=")
            os.system('cls')
            if continuar == '1':
                break  # volta para cadastrar outro livro
            elif continuar == '2':
                voltando()
                return
            else:
                print("Digite 1 para continuar cadastrando outros livros, ou 2 para voltar ao menu inicial!")

def alterar_livro():
    mostrar_livros()
    global livros
    try:
        print(20*"-=")
        posicao = int(input("\nDigite a posição do livro que deseja alterar, ou aperte qualquer tecla para voltar.\n")) - 1
        if 0 <= posicao < len(livros):
            print(20*"-=")
            novo_titulo = input("\nDigite o novo nome do livro: ")
            novo_genero = input("Digite o novo gênero do livro: ")
            livros[posicao]["titulo"] = novo_titulo
            livros[posicao]["genero"] = novo_genero

            salvar_livros(livros)

            print(20*"-=")
            input(f"\nLivro na posição {posicao + 1} atualizado com sucesso! Aperte qualquer tecla para voltar.\n")
            voltando()
        else:
            print("Posição inválida.")
    except ValueError:
        voltando()
        os.system('cls')


def livros_cadastrados_menu():
    while True:
        os.system('cls')
        mostrar_livros()
        menu_livros = input("\n1) Excluir algum livro \n2) Visualizar conteúdo de um livro \n3) Voltar\n")
        if menu_livros == '1':
            os.system('cls')
            mostrar_livros()
            try:
                livro_escolha = int(input("\nEscolha o número do livro para excluir: "))
                if 1 <= livro_escolha <= len(livros):
                    livro_removido = livros.pop(livro_escolha - 1)
                    salvar_livros(livros)  # salva a lista atualizada no JSON
                    os.system('cls')
                    print(f"O livro '{livro_removido['titulo']}' foi removido da Livraria.")
                else:
                    print("Escolha de livro inválida.")
            except ValueError:
                print("Entrada inválida.")
            input("\nAperte qualquer tecla pra voltar para o menu.")
            voltando()
        elif menu_livros == '2':
            os.system('cls')
            mostrar_livros()
            try:
                posicao = int(input("\nEscolha a posição do livro que você deseja ler, ou aperte qualquer tecla para voltar.\n")) - 1
                os.system('cls')
                if 0 <= posicao < len(livros):
                    print("\nQuando quiser sair deste livro, apenas precione qualquer tecla.")
                    print(35*"-=")
                    print(f"\n\n\n                                         {livros[posicao]['titulo']}.\n")
                    texto()
                    input('')
                    voltando()
                else:
                    print("Não existe livro nesta posição, tente novamente!")
            except ValueError:
                voltando()
        elif menu_livros == '3':
            os.system('cls')
            voltando()
            break
        else:
            print("Você deve escolher uma das opções abaixo, (1-3).")
        os.system('cls')

def usuarios_cadastrados_menu():
    os.system('cls')
    while True:
        try:
            with open('db/usuarios.json', 'r') as f:
                dados = json.load(f)
                usuarios = dados.get("usuarios", [])
                senhas = dados.get("senhas", {})
                bibliotecas = dados.get("bibliotecas", {})
        except FileNotFoundError:
            print("Nenhum usuário cadastrado.")
            voltando()
            break

        usuarios_sem_admin = [user for user in usuarios if user != "admin"]

        if not usuarios_sem_admin:
            print("Nenhum usuário cadastrado (além do admin).")
            voltando()
            break

        print("\nUsuários cadastrados:")
        for i, usuario in enumerate(usuarios_sem_admin, 1):
            print(f"{i} - {usuario}")

        menu_usuarios = input("\n1) Excluir um usuário \n2) Visualizar biblioteca de usuário \n3) Voltar\n")
        if menu_usuarios == '1':
            os.system('cls')
            print("\nUsuários cadastrados:")
            for i, usuario in enumerate(usuarios_sem_admin, 1):
                print(f"{i} - {usuario}")

            try:
                usuario_escolha = int(input("\nEscolha o número do usuário para excluir. \nOu aperte qualquer tecla para voltar.\n"))
                if 1 <= usuario_escolha <= len(usuarios_sem_admin):
                    usuario_removido = usuarios_sem_admin[usuario_escolha - 1]

                    print(f"\nVocê tem certeza que deseja excluir o usuário '{usuario_removido}'?")
                    print("Este usuário irá perder toda sua biblioteca!")

                    confirmacao = input("\n1 - Sim\n2 - Não\nEscolha: ")
                    if confirmacao == '1':
                        usuarios.remove(usuario_removido)
                        senhas.pop(usuario_removido, None)
                        bibliotecas.pop(usuario_removido, None)

                        dados["usuarios"] = usuarios
                        dados["senhas"] = senhas
                        dados["bibliotecas"] = bibliotecas

                        with open('db/usuarios.json', 'w') as f:
                            json.dump(dados, f, indent=4)

                        print(f"\nUsuário '{usuario_removido}' foi removido com sucesso!")
                        input("\nPressione qualquer tecla para voltar.")
                    else:
                        print("\nExclusão cancelada.")
                        input("\nPressione qualquer tecla para voltar.")
                else:
                    print("Escolha inválida.")
                    input("\nPressione qualquer tecla para voltar.")
            except ValueError:
                voltando()
        elif menu_usuarios == '2':
            os.system('cls')
            print("\nUsuários cadastrados:")
            for i, usuario in enumerate(usuarios_sem_admin, 1):
                print(f"{i} - {usuario}")

            try:
                escolha = int(input("\nEscolha o número do usuário para visualizar a biblioteca. \nOu aperte qualquer tecla para voltar.\n"))
                if 1 <= escolha <= len(usuarios_sem_admin):
                    usuario_escolhido = usuarios_sem_admin[escolha - 1]
                    livros_user = bibliotecas.get(usuario_escolhido, [])
                    print(f"\nBiblioteca de {usuario_escolhido}:")
                    if livros_user:
                        for idx, livro in enumerate(livros_user, 1):
                            print(f"{idx} - {livro['titulo']} ({livro['genero']})")
                    else:
                        print("Este usuário não possui livros cadastrados.")
                    input("\nPressione qualquer tecla para voltar.")
                else:
                    print("Escolha inválida.")
                    input("\nPressione qualquer tecla para voltar.")
            except ValueError:
                voltando()
        elif menu_usuarios == '3':
            voltando()
            break
        else:
            print("Você deve escolher uma das opções abaixo, (1-3).")

def buscar_novos_livros(lista_livros, livros_lidos):
    # Retorna a lista de livros que o usuário ainda não leu
    novos = [livro for livro in lista_livros if livro not in livros_lidos]
    return novos

def biblioteca_usuario_menu(biblioteca_pessoal, lista_livros):
    while True:
        dados = carregar_usuarios()
        print("\n=== Biblioteca do Usuário ===")
        print("1 - Ler livros salvos")
        print("2 - Remover livros")
        print("0 - Voltar")
        escolha = input("Escolha: ")

        if escolha == "1":
            if biblioteca_pessoal:
                print("\nLivros salvos:")
                for i, livro in enumerate(biblioteca_pessoal, start=1):
                    print(f"{i}. {livro['titulo']} - {livro['genero']}")

                while True:
                    escolha_livro = input("\nDigite o número do livro que deseja ler ou 0 para voltar: ")

                    if escolha_livro.isdigit():
                        escolha_livro = int(escolha_livro)
                        if escolha_livro == 0:
                            break
                        elif 1 <= escolha_livro <= len(biblioteca_pessoal):
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print("\nQuando quiser sair deste livro, apenas pressione qualquer tecla.")
                            print(35 * "-=")
                            print(f"\n\n\n                                         {biblioteca_pessoal[escolha_livro - 1]['titulo']}.\n")
                            texto()  # Exibe o conteúdo do livro
                            input('')
                            voltando()
                            break
                        else:
                            print("Número inválido. Tente novamente.")
                    else:
                        print("Digite apenas números.")
            else:
                print("Nenhum livro salvo na biblioteca.")


        elif escolha == "2":
            if not biblioteca_pessoal:
                print("Nenhum livro para remover.")
            else:
                print("Livros salvos:")
                for idx, livro in enumerate(biblioteca_pessoal, 1):
                    print(f"{idx} - {livro['titulo']} - {livro['genero']}")
                escolha_livro = input("Digite o número do livro para remover: ")
                if escolha_livro.isdigit():
                    escolha_livro = int(escolha_livro)
                    if 1 <= escolha_livro <= len(biblioteca_pessoal):
                        removido = biblioteca_pessoal.pop(escolha_livro - 1)
                        print(f"Livro '{removido['titulo']}' removido com sucesso.")
                    else:
                        print("Opção inválida.")
                else:
                    print("Entrada inválida.")
        elif escolha == "0":
            break
        else:
            print("Opção inválida, tente novamente.")


def atualizar_dados_usuario(dados, usuario_antigo, novo_usuario=None, nova_senha=None):
    if novo_usuario and novo_usuario != usuario_antigo:
        if usuario_antigo in dados['usuarios']:
            dados['usuarios'].remove(usuario_antigo)
            dados['usuarios'].append(novo_usuario)

        if usuario_antigo in dados['senhas']:
            dados['senhas'][novo_usuario] = dados['senhas'].pop(usuario_antigo)

        if usuario_antigo in dados['bibliotecas']:
            dados['bibliotecas'][novo_usuario] = dados['bibliotecas'].pop(usuario_antigo)

    if nova_senha:
        if novo_usuario:
            dados['senhas'][novo_usuario] = nova_senha
        else:
            dados['senhas'][usuario_antigo] = nova_senha

    return dados


def alterar_conta(usuarios, senhas, bibliotecas, usuario_atual):
    print("\n=== Alterar Conta ===")
    print("1 - Alterar usuário")
    print("2 - Alterar senha")
    print("3 - Excluir conta")
    print("0 - Voltar")
    escolha = input("Escolha: ")

    if escolha == "1":
        novo_usuario = input("Digite o novo nome de usuário: ")
        if novo_usuario in usuarios:
            print("Nome de usuário já existe.")
            return usuario_atual
        else:
            idx = usuarios.index(usuario_atual)
            usuarios[idx] = novo_usuario
            senhas[novo_usuario] = senhas.pop(usuario_atual)
            bibliotecas[novo_usuario] = bibliotecas.pop(usuario_atual)
            print("Usuário alterado com sucesso.")
            return novo_usuario

    elif escolha == "2":
        nova_senha = input("Digite a nova senha: ")
        senhas[usuario_atual] = nova_senha
        print("Senha alterada com sucesso.")
        return usuario_atual

    elif escolha == "3":
        usuario_confirm = input("Digite seu nome de usuário para confirmar: ")
        senha_confirm = input("Digite sua senha para confirmar: ")

        if usuario_confirm == usuario_atual and senhas.get(usuario_confirm) == senha_confirm:
            print("Você irá perder toda sua biblioteca, confirma exclusão de conta?")
            print("1 - Sim")
            print("2 - Não")
            confirma = input("Escolha: ")
            if confirma == "1":
                usuarios.remove(usuario_atual)
                senhas.pop(usuario_atual, None)
                bibliotecas.pop(usuario_atual, None)
                print("Conta excluída com sucesso.")
                return None  # Sinaliza que a conta foi excluída
            else:
                print("Exclusão cancelada.")
                return usuario_atual
        else:
            print("Usuário ou senha incorretos. Exclusão cancelada.")
            return usuario_atual

    elif escolha == "0":
        return usuario_atual

    else:
        print("Opção inválida.")
        return usuario_atual


def carregar_usuarios(arquivo='db/usuarios.json'):
    if not os.path.exists(arquivo):
        dados = {
            "usuarios": ["admin"],
            "senhas": {"admin": "admin"},
            "bibliotecas": {"admin": []}
        }
        salvar_usuarios(dados, arquivo)
        return dados

    try:
        with open(arquivo, 'r') as f:
            conteudo = f.read().strip()
            if not conteudo:
                dados = {
                    "usuarios": ["admin"],
                    "senhas": {"admin": "admin"},
                    "bibliotecas": {"admin": []}
                }
                salvar_usuarios(dados, arquivo)
                return dados

            dados = json.loads(conteudo)

            # Corrigir formato antigo (se existir)
            if "usuarios" not in dados or "senhas" not in dados or "bibliotecas" not in dados:
                # Formato antigo -> cria novo
                dados = {
                    "usuarios": ["admin"],
                    "senhas": {"admin": "admin"},
                    "bibliotecas": {"admin": []}
                }
                salvar_usuarios(dados, arquivo)
                return dados

            # Adiciona admin se não tiver
            if "admin" not in dados["usuarios"]:
                dados["usuarios"].append("admin")
                dados["senhas"]["admin"] = "admin"
                dados["bibliotecas"]["admin"] = []

            # Corrigir livros salvos como strings
            for user, livros_user in dados["bibliotecas"].items():
                novos_livros = []
                for livro in livros_user:
                    if isinstance(livro, str):
                        livro_catalogo = next((l for l in livros if l["titulo"] == livro), None)
                        if livro_catalogo:
                            novos_livros.append(livro_catalogo)
                        else:
                            pass  # Ignora livros que não existem mais no catálogo
                    else:
                        novos_livros.append(livro)
                dados["bibliotecas"][user] = novos_livros

            salvar_usuarios(dados, arquivo)
            return dados

    except (FileNotFoundError, json.JSONDecodeError):
        dados = {
            "usuarios": ["admin"],
            "senhas": {"admin": "admin"},
            "bibliotecas": {"admin": []}
        }
        salvar_usuarios(dados, arquivo)
        return dados

def salvar_usuarios(dados, arquivo='db/usuarios.json'):
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)


def salvar_dados(dados, arquivo='dados.json'):
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)


def carregar_livros():
    if not os.path.exists(CAMINHO_LIVROS):
        with open(CAMINHO_LIVROS, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
        return []
    with open(CAMINHO_LIVROS, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_livros(lista_livros):
    with open(CAMINHO_LIVROS, "w", encoding="utf-8") as f:
        json.dump(lista_livros, f, ensure_ascii=False, indent=4)

# Inicialmente carrega os livros em memória
livros = carregar_livros()


# MENU ADMIN
def menu_admin():
    while True:
        menu = input("\nAcesso restrito para Administrador \n1) Cadastro de um novo livro \n2) Alterar nome e gênero de um livro \n3) Livros cadastrados \n4) Usuários cadastrados \n5) Sair da conta\n")
        print(35*"-=")
        if menu == "1":
            cadastro_novo_livro()
        elif menu == "2":
            alterar_livro()
        elif menu == "3":
            livros_cadastrados_menu()
        elif menu == "4":
            usuarios_cadastrados_menu()
        elif menu == "5":
            os.system('cls')
            saindo()
            break
        else:
            os.system('cls')
            print("Você deve escolher uma das opções abaixo, (1-5).")

# MENU USUARIO
def menu_usuario(usuario):
    while True:
        print("Olá", usuario, "Seja bem vindo.\n")
        menu = input("Escolha o que quer: \n1) Adicionar livros à sua biblioteca \n2) Sua biblioteca (ver, ler e excluir livros) \n3) Alterar sua conta \n4) Sair da conta\n")
        print(35*"-=")
        os.system('cls')

        dados = carregar_usuarios()

        if usuario not in dados['bibliotecas']:
            dados['bibliotecas'][usuario] = []

        biblioteca_pessoal = dados['bibliotecas'][usuario]

        if menu == "1":
            adicionar_livro_menu(biblioteca_pessoal, dados)
            salvar_usuarios(dados)

        elif menu == "2":
            biblioteca_usuario_menu(biblioteca_pessoal, livros)
            salvar_usuarios(dados)

        elif menu == "3":
            novo_usuario = alterar_conta(dados['usuarios'], dados['senhas'], dados['bibliotecas'], usuario)
            if novo_usuario is None:
                # Conta excluída, sai do menu
                salvar_usuarios(dados)
                print("Saindo... Sua conta foi excluída.")
                time.sleep(2)
                break
            elif novo_usuario != usuario:
                usuario = novo_usuario
            salvar_usuarios(dados)

        elif menu == "4":
            saindo()
            break

        else:
            print("Escolha uma das opções válidas (1-4)")
            time.sleep(2)

        os.system('cls')

def adicionar_livro_menu(biblioteca_pessoal, dados):
    titulos_biblioteca = {livro['titulo'] for livro in biblioteca_pessoal}
    livros_disponiveis = [livro for livro in livros if livro['titulo'] not in titulos_biblioteca]

    if not livros_disponiveis:
        print("Nenhum livro novo para adicionar.")
        time.sleep(2)
        return

    print("Livros disponíveis para adicionar:")
    for idx, livro in enumerate(livros_disponiveis, 1):
        print(f"{idx} - {livro['titulo']} - {livro['genero']}")

    escolha_livro = input("Digite o número do livro para adicionar (ou 0 para voltar): ")
    if escolha_livro.isdigit():
        escolha_livro = int(escolha_livro)
        if escolha_livro == 0:
            return
        if 1 <= escolha_livro <= len(livros_disponiveis):
            livro_escolhido = livros_disponiveis[escolha_livro - 1]
            biblioteca_pessoal.append(livro_escolhido)
            print(f"Livro '{livro_escolhido['titulo']}' adicionado com sucesso.")
            time.sleep(2)
        else:
            print("Opção inválida.")
            time.sleep(2)
    else:
        print("Entrada inválida.")
        time.sleep(2)

