import os
import time
import json

from core.db import livros, generos, usuarios, senhas, bibliotecas

def voltando():
    time.sleep(1)
    os.system('cls')

def saindo():
    print("Saindo da conta...")

def mostrar_livros():
    print("Livros cadastrados:")
    for i, (livro, genero) in enumerate(zip(livros, generos), 1):
        print(f"{i} - {livro} ({genero})")

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
    while True:
        livro = input("Nome do livro: ")
        if livro == 'voltar':
            voltando()
            break
        genero = input("Gênero do livro: ")
        livros.append(livro)
        generos.append(genero)
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
    try:
        print(20*"-=")
        posicao = int(input("\nDigite a posição do livro que deseja alterar, ou aperte qualquer tecla para voltar.\n")) - 1
        if 0 <= posicao < len(livros):
            print(20*"-=")
            novo_titulo = input("\nDigite o novo nome do livro: ")
            novo_genero = input("Digite o novo gênero do livro: ")
            livros[posicao] = novo_titulo
            generos[posicao] = novo_genero
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
                    generos.pop(livro_escolha - 1)
                    os.system('cls')
                    print(f"O livro '{livro_removido}' foi removido da Livraria.")
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
                    print(f"\n\n\n                                         {livros[posicao]}.\n")
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
        if len(usuarios) <= 1 or not usuarios[1]:
            mostrar_usuarios()
            voltando()
            break
        else:
            mostrar_usuarios()
            menu_usuarios = input("\n1) Excluir um usuário \n2) Visualizar biblioteca de usuário \n3) Voltar\n")
            if menu_usuarios == '1':
                while True:
                    os.system('cls')
                    mostrar_usuarios()
                    try:
                        usuario_escolha = int(input("\nEscolha o número do usuário para excluir. \nOu aperte qualquer tecla para voltar.\n"))
                        if 1 <= usuario_escolha < len(usuarios):
                            usuario_removido = usuarios.pop(usuario_escolha)
                            bibliotecas.pop(usuario_removido, None)
                            print(f"Foi removido o cadastro de '{usuario_removido}' da Livraria.\n")
                            break
                        else:
                            print("Escolha de usuário inválida, tente novamente")
                    except:
                        voltando()
                        break
            elif menu_usuarios == '2':
                os.system('cls')
                while True:
                    try:
                        mostrar_usuarios()
                        print(20 * "-=")
                        posicao = int(input("\nEscolha a posição do usuário que deseja verificar sua biblioteca. \nOu aperte qualquer tecla para voltar.\n")) - 1
                        os.system('cls')
                        if 0 <= posicao < (len(usuarios) - 1):
                            usuario_selecionado = usuarios[posicao + 1]
                            livros_user = bibliotecas.get(usuario_selecionado, [])
                            print(20 * "-=")
                            print("\nUsuário:", usuario_selecionado)
                            if not livros_user:
                                print("Este usuário não tem nenhum livro na sua biblioteca.")
                            else:
                                for i, livro in enumerate(livros_user, 1):
                                    print(f"{i} - {livro}")
                            input("\nPressione qualquer tecla para voltar.")
                            voltando()
                        else:
                            print("Não existe usuário nesta posição, tente novamente!")
                    except ValueError:
                        voltando()
                        break
                os.system('cls')
            elif menu_usuarios == '3':
                voltando()
                break
            else:
                print("Você deve escolher uma das opções abaixo, (1-3).")
    os.system('cls')

def buscar_novos_livros(lista_livros, livros_lidos):
    # Retorna a lista de livros que o usuário ainda não leu
    novos = [livro for livro in lista_livros if livro not in livros_lidos]
    return novos


def biblioteca_usuario_menu(biblioteca_pessoal, lista_livros):
    while True:
        print("\n=== Biblioteca do Usuário ===")
        print("1 - Ver livros salvos")
        print("2 - Adicionar livro")
        print("3 - Remover livro")
        print("0 - Voltar")
        escolha = input("Escolha: ")

        if escolha == "1":
            if biblioteca_pessoal:
                print("Livros salvos:")
                for livro in biblioteca_pessoal:
                    print(f"- {livro}")
            else:
                print("Nenhum livro salvo na biblioteca.")
        elif escolha == "2":
            novos_livros = buscar_novos_livros(lista_livros, biblioteca_pessoal)
            if not novos_livros:
                print("Nenhum livro novo para adicionar.")
            else:
                print("Livros disponíveis para adicionar:")
                for idx, livro in enumerate(novos_livros, 1):
                    print(f"{idx} - {livro}")
                escolha_livro = input("Digite o número do livro para adicionar: ")
                if escolha_livro.isdigit():
                    escolha_livro = int(escolha_livro)
                    if 1 <= escolha_livro <= len(novos_livros):
                        biblioteca_pessoal.append(novos_livros[escolha_livro - 1])
                        print("Livro adicionado com sucesso.")
                    else:
                        print("Opção inválida.")
                else:
                    print("Entrada inválida.")
        elif escolha == "3":
            if not biblioteca_pessoal:
                print("Nenhum livro para remover.")
            else:
                print("Livros salvos:")
                for idx, livro in enumerate(biblioteca_pessoal, 1):
                    print(f"{idx} - {livro}")
                escolha_livro = input("Digite o número do livro para remover: ")
                if escolha_livro.isdigit():
                    escolha_livro = int(escolha_livro)
                    if 1 <= escolha_livro <= len(biblioteca_pessoal):
                        removido = biblioteca_pessoal.pop(escolha_livro - 1)
                        print(f"Livro '{removido}' removido com sucesso.")
                    else:
                        print("Opção inválida.")
                else:
                    print("Entrada inválida.")
        elif escolha == "0":
            break
        else:
            print("Opção inválida, tente novamente.")


def alterar_conta(usuarios, senhas, usuario_atual):
    print("\n=== Alterar Conta ===")
    print("1 - Alterar usuário")
    print("2 - Alterar senha")
    print("0 - Voltar")
    escolha = input("Escolha: ")

    if escolha == "1":
        novo_usuario = input("Digite o novo nome de usuário: ")
        if novo_usuario in usuarios:
            print("Nome de usuário já existe.")
        else:
            idx = usuarios.index(usuario_atual)
            usuarios[idx] = novo_usuario
            print("Usuário alterado com sucesso.")
            return novo_usuario  # Atualiza o usuário atual
    elif escolha == "2":
        nova_senha = input("Digite a nova senha: ")
        idx = usuarios.index(usuario_atual)
        senhas[idx] = nova_senha
        print("Senha alterada com sucesso.")
    elif escolha == "0":
        return usuario_atual
    else:
        print("Opção inválida.")
    return usuario_atual

def carregar_usuarios(arquivo='usuarios.json'):
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'usuarios': [],
            'senhas': {},
            'bibliotecas': {}
        }

def salvar_usuarios(dados, arquivo='usuarios.json'):
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)


def salvar_dados(dados, arquivo='dados.json'):
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)




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
        menu = input("Escolha o que quer: \n1) Buscar novos livros \n2) Sua bibliotéca \n3) Alterar sua conta \n4) Sair do conta\n")
        print(35*"-=")
        os.system('cls')

        if menu == "1":
            buscar_novos_livros(usuario)
        elif menu == "2":
            biblioteca_usuario_menu(usuario)
        elif menu == "3":
            alterar_conta(usuario)
        elif menu == "4":
            saindo()
            break
        else:
            print("Escolha uma das opções válidas (1-4)")
            


# Implemente as funções buscar_novos_livros, biblioteca_usuario_menu e alterar_conta conforme seu código original.