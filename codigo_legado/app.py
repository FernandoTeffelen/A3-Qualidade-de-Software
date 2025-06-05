import os
import time
from defs import *
from db import *


while True: # parar nunca encerrar o código
    while True: # fazer cadastro ou login
        # print(f"Temos {usuarios} usuarios.")
        # print(f"Com um total de {len(usuarios)} usuarios.\n\n")
        temCadastro = input("Você ja possui cadastro? \n1)sim \n2)não\n")
        os.system('cls')
        
        if temCadastro == '1':
            print("Entrar na conta")
            print(20*"-=")
            usuario = input("Usuário: ")
            senha = input("Senha: ")
            os.system('cls')
            break
        
        elif temCadastro == '2':
            print("\nVamos fazer seu cadastro")
            print(20*"-=")
            # fazer o cadastro
            while True:
                usuario = input("Digite qual vai ser seu usuário: ")
                senha = input("Escolha sua senha: ")
                if usuario == usuarios[0] and senha == senhas[0]:
                    break
                if usuario in usuarios:
                    os.system('cls')
                    print("Usuario ja utilizado, tente outro!")
                elif usuario == '':
                    os.system('cls')
                    print("Seu usuario deve conter ao menos 1 caracter")
                elif len(senha) < 6:
                    os.system('cls')
                    print("Sua senha devem possuir ao menos 6 caracteres")
                else:
                    usuarios.append(usuario)
                    senhas.append(senha)
                    bibliotecas[usuario] = []
                    os.system('cls')
                    print("Cadastro realizado com sucesso!")
                    break
            if (usuario == usuarios[0] and senha == senhas[0]):
                os.system('cls')
                break
        elif temCadastro != '1' or temCadastro != '2':
            os.system('cls')
            print("Digite uma das duas opções, 1 ou 2.")
    
    # entra na conta
    while True:
        # ADMIN
        if (usuario == usuarios[0] or senha == senhas[0]):
            while True:
                # print(bibliotecas)
                menu = input("\nAcesso restrito para Administrador \n1) Cadastro de um novo livro \n2) Alterar nome e gênero de um livro \n3) Livros cadastrados \n4) Usuarios cadastrados \n5) Sair da conta\n")
                print(35*"-=")
                    
                if (menu == "1"):
                    os.system('cls')
                    print("Cadastro de um novo livro.\nOu digite \"voltar\", para voltar ao menu.\n")
                    print(20*"-=")
                    livro = input("Nome do livro: ")
                    if livro == 'voltar':
                        voltando()
                    else:
                        genero = input("Gênero do livro: ")
                        livros.append(livro)
                        generos.append(genero)
                        os.system('cls')

                        while True: 
                            continuar = input("Deseja cadastrar outro livro? \n1) sim \n2) não\n")
                            print(20*"-=")
                            os.system('cls')

                            # continuar o cadastro de mais livros
                            if (continuar == '1'):
                                livro = input("Nome do livro: ")
                                genero = input("Gênero do livro: ")
                                livros.append(livro)
                                generos.append(genero)
                                os.system('cls')
                            elif (continuar == '2'):
                                voltando()
                                break
                            else:
                                print("Digite 1 para continuar cadastrando outros livros, ou 2 para voltar ao menu inicial!")
                    os.system('cls')


                elif (menu == "2"):
                    mostrar_livros()
                    try:
                        print(20*"-=")
                        posicao = int(input("\nDigite a posição do livro que deseja alterar, ou aperte qualquer tecla para voltar.\n")) - 1
                        
                        if 0 <= posicao < len(livros):
                            print(20*"-=")
                            novo_titulo = input("\nDigite o novo nome do livro: ")
                            novo_genero = input("Digite o novo gênero do livro: ")
                            
                            livros[posicao] = novo_titulo    # Atualiza o título na posição especificada
                            generos[posicao] = novo_genero  # Atualiza o gênero na posição especificada
                            print(20*"-=")
                            input(f"\nLivro na posição {posicao + 1} atualizado com sucesso! Aperte qualquer tecla para voltar.\n")
                            voltando()
                            
                        else:
                            print("Posição inválida.")
                    
                    except ValueError:
                        voltando()
                        os.system('cls')


                elif (menu == "3"):
                    while True:
                        os.system('cls')
                        mostrar_livros()
                        menu_livros = input("\n1) Excluir algum livro \n2) vizualizar conteudo de um livro \n3) voltar\n")
                        
                        if menu_livros == '1':
                            # Escolhe o livro para excluir
                            os.system('cls')
                            mostrar_livros()
                            livro_escolha = int(input("\nEscolha o número do livro para excluir: "))
                            if 1 <= livro_escolha <= len(livros):
                                os.system('cls')
                                livro_removido = livros.pop(livro_escolha - 1)
                                print(f"O livro '{livro_removido}' foi removido da Livraria.")
                            else:
                                print("Escolha de livro inválida.")
                            input("\nAperte qualquer tecla pra voltar para o menu.")
                            os.system('cls')
                            voltando()
                        elif menu_livros == '2':
                            os.system('cls')
                            mostrar_livros()
                            posicao = int(input("\nEscolha a posição do livro que você deseja ler, ou aperte qualquer tecla para voltar.\n")) - 1
                            os.system('cls')
                            if 0 <= posicao < len(livros):  # Verifica se a posição é válida
                                print("\nQuando quiser sair deste livro, apenas precione qualquer tecla.")
                                print(35*"-=")
                                print(f"\n\n\n                                         {livros[posicao]}.\n")
                                texto()
                                input('')
                                os.system('cls')
                                voltando()
                            else:
                                print("Não existe livro nesta posição, tente novamente!")
                        elif menu_livros == '3':
                            os.system('cls')
                            voltando()
                            break
                        else:
                            print("Você deve escolher uma das opções abaixo, (1-3).")
                        os.system('cls')

                elif (menu == "4"):
                    os.system('cls')
                    while True:
                        if len(usuarios) <= 1 or not usuarios[1]:
                            mostra_usuarios()
                            voltando()
                            break
                        else:
                            mostra_usuarios()
                            menu_usuarios = input("\n1) Excluir um usuário \n2) Visualizar biblioteca de usuário \n3) Voltar\n")
                            if menu_usuarios == '1':
                                while True:
                                    os.system('cls')
                                    mostra_usuarios()
                                    try:
                                        usuario_escolha = int(input("\nEscolha o número do usuário para excluir. \nOu aperte qualquer tecla para voltar.\n"))
                                        
                                        if 1 <= usuario_escolha < len(usuarios):  
                                            os.system('cls')
                                            usuario_removido = usuarios.pop(usuario_escolha)
                                            bibliotecas.pop(usuario_removido, None)  # Remove a biblioteca do usuário, se existir
                                            print(f"Foi removido o cadastro de '{usuario_removido}' da Livraria.\n")
                                            break
                                        else:
                                            os.system('cls')
                                            print("Escolha de usuário inválida, tente novamente")
                                    except:
                                        voltando()
                                        break
                            elif menu_usuarios == '2':
                                os.system('cls')
                                while True:
                                    try:
                                        mostra_usuarios()
                                        print(20 * "-=")
                                        posicao = int(input("\nEscolha a posição do usuário que deseja verificar sua biblioteca. \nOu aperte qualquer tecla para voltar.\n")) - 1
                                        os.system('cls')
                                        
                                        if 0 <= posicao < (len(usuarios) - 1):  # Verifica se a posição é válida
                                            usuario_selecionado = usuarios[posicao + 1]  # Corrige o índice para evitar erro
                                            livros = bibliotecas.get(usuario_selecionado, [])
                                            
                                            # Exibe a biblioteca do usuário selecionado
                                            print(20 * "-=")
                                            print("\nUsuário:", usuario_selecionado)
                                            if not livros:
                                                print("Este usuário não tem nenhum livro na sua biblioteca.")
                                            else:
                                                for i, livro in enumerate(livros, 1):
                                                    print(f"{i} - {livro}")

                                            input("\nPressione qualquer tecla para voltar.")
                                            voltando()
                                        else:
                                            os.system('cls')
                                            print("Não existe usuário nesta posição, tente novamente!")
                                    except ValueError:
                                        voltando()
                                        break
                                os.system('cls')
                            elif menu_usuarios == '3':
                                voltando()
                                break
                            else:
                                os.system('cls')
                                print("Você deve escolher uma das opções abaixo, (1-3).")
                    os.system('cls')
                        
                elif (menu == "5"):
                    os.system('cls')
                    saindo()
                    break
                else:
                    os.system('cls')
                    print("Você deve escolher uma das opções abaixo, (1-5).")
                    
            # sair para area de cadastro
            if 1 == 1:
                break

        # USUARIO
        elif (usuario in usuarios and senha in senhas):
            usuarioCadastrado = usuario
            senhaCadastrada = senha
            while True:
                print("Olá", usuario, "Seja bem vindo.\n")
                menu = input("Escolha o que quer: \n1) Buscar novos livros \n2) Sua bibliotéca \n3) Alterar sua conta \n4) Sair do conta\n")
                print(35*"-=")
                os.system('cls')
                
                if (menu == "1"):
                    while True:
                        mostrar_livros()
                        separar = input("\nDeseja separar a bibliotéca por gênero? \n1) Sim \n2) Não \n3) Voltar\n")
                        os.system('cls')

                        if (separar == '1'):
                            while True:
                                print("\naventura      biografia\nclássico      distopia\ndrama         fantasia\nficção        filosófico\nPortuguês     infantil\nmistério      poesia\nromance       suspense\nterror        tragédia\n")
                                print(20*"-=")
                                qualGenero = input("Escolha o gênero de livro que deseja ver, ou digite \"voltar\", para voltar ao menu.\n").strip().lower()
                                if qualGenero == 'voltar':
                                    voltando()
                                    break
                                elif qualGenero in generos_map:   # Verificação do gênero
                                    genero_escolhido = generos_map[qualGenero]
                                    livros_por_genero(genero_escolhido)
                                    try:
                                        posicao = int(input("\nEscolha a posição do livro que você deseja pegar, ou aperte qualquer tecla para voltar.\n")) - 1
                                        os.system('cls')
                                        if 0 <= posicao < len(livros):  # Verificação se contem a posição escolhida
                                            if livros[posicao] in bibliotecas[usuario]: # Verifica se o livro já está na biblioteca do usuário
                                                print("O livro escolhido já está na sua biblioteca, por favor, escolha outro.")
                                            else:
                                                if posicao not in livros_por_genero(genero_escolhido):  #Verifica se a posição pertence a este genero
                                                    os.system('cls')
                                                    print("Este livro não pertence a este gênero, por favor tente novamente.")
                                                else:
                                                    os.system('cls')
                                                    adicionar_livro(usuario, posicao)
                                                    print(f"O livro '{livros[posicao]}' foi adicionado à sua biblioteca.")
                                                    time.sleep(2)
                                                    voltando()
                                                    break
                                    except ValueError:
                                        voltando()
                                else:
                                    os.system('cls')
                                    print("Gênero não encontrado, tente novamente!")
                        elif (separar == '2'):
                            print("\n\n")
                            mostrar_livros()
                            print("\nTudo bem.\n")
                            while True:
                                try:
                                    posicao = int(input("\nEscolha a posição do livro que você deseja pegar, ou aperte qualquer tecla para voltar.\n")) - 1
                                    os.system('cls')
                                    if 0 <= posicao < len(livros):  # Verifica se a posição é válida
                                        if livros[posicao] in bibliotecas[usuario]: # Verifica se o livro já está na biblioteca do usuário
                                            mostrar_livros()
                                            print("\nO livro escolhido já está na sua biblioteca, por favor, escolha outro.")
                                        else:
                                            adicionar_livro(usuario, posicao)
                                            print(f"O livro '{livros[posicao]}' foi adicionado à sua biblioteca.")
                                            time.sleep(2)
                                            voltando()
                                            break
                                    else:
                                        mostrar_livros()
                                        print("\nNão existe livro nesta posição, tente novamente!")
                                except ValueError:
                                    voltando()
                                    break
                        elif (separar == '3'):
                            voltando()
                            break
                        else:
                            print("\n\nEscolha uma das opções validas(1-3)\n")

                elif (menu == "2"):
                    os.system('cls')
                    if not bibliotecas[usuario]:
                        biblioteca_usuario(usuario)
                        voltando()
                    else:
                        while True:
                            biblioteca_usuario(usuario)
                            print(20*"-=")
                            try:
                                escolha = input("1) Excluir algum livro da bibliotéca \n2) Ler algum livro \n3) Voltar\n")
                                if escolha == '1':
                                    os.system('cls')
                                    print(f"\nVocê tem os seguintes livros:\n")
                                    for i, livro in enumerate(bibliotecas[usuario], 1):
                                        print(f"{i} - {livro}\n")
                                    
                                    # Escolhe o livro para excluir
                                    livro_escolha = int(input("\nEscolha o número do livro para excluir: "))
                                    if 1 <= livro_escolha <= len(bibliotecas[usuario]):
                                        os.system('cls')
                                        livro_removido = bibliotecas[usuario].pop(livro_escolha - 1)
                                        print(f"O livro '{livro_removido}' foi removido da biblioteca de {usuario}.")
                                    else:
                                        print("Escolha de livro inválida.")

                                elif escolha == '2':
                                    os.system('cls')
                                    biblioteca_usuario(usuario)
                                    posicao = int(input("\nEscolha a posição do livro que você deseja ler, ou aperte qualquer tecla para voltar.\n")) - 1
                                    os.system('cls')
                                    if 0 <= posicao < len(bibliotecas[usuario]):  # Verifica se a posição é válida
                                        print("\nQuando quiser sair deste livro, apenas precione qualquer tecla.")
                                        print(35*"-=")
                                        print(f"\n\n\n                                         {bibliotecas[usuario][posicao]}.\n")
                                        texto()
                                        input('')
                                        voltando()
                                    else:
                                        print("Não existe livro nesta posição, tente novamente!")
                                elif escolha == '3':
                                    voltando()
                                    break
                                else:
                                    os.system('cls')
                                    print("\n\nEscolha uma das opções validas(1-3)\n")
                                
                            except ValueError:
                                voltando()
                                break

                elif (menu == "3"):
                    os.system('cls')
                    while True:
                        print("Vamos certificar de que é você, ou digite \"voltar\", para voltar ao menu!")
                        print("-=" * 10)
                        # indentificar se o usuario deseja voltar ao menu, pelo usuario ou senha
                        usuario = input("Usuário: ")
                        if usuario == 'voltar':
                            usuario = usuarioCadastrado
                            voltando()
                            break
                        senha = input("Senha: ")
                        if senha == 'voltar':
                            usuario = usuarioCadastrado
                            voltando()
                            break
                        os.system('cls')
                        if (usuario == usuarioCadastrado and senha == senhaCadastrada):
                            while True:
                                novo_usuario = input("\nDigite seu novo nome de usuário: ")
                                nova_senha = input("Digite sua novo senha: ")
                                if novo_usuario == '':
                                    os.system('cls')
                                    print("\nSeu usuario devem possuir ao menos 1 caracter")
                                elif len(nova_senha) < 6:
                                    os.system('cls')
                                    print("\nSua senha devem possuir ao menos 6 caracteres")
                                else:
                                    if novo_usuario in usuarios:
                                        os.system('cls')
                                        print("\nEste usuario ja esta em uso. Favor escolher outro usuario!")
                                    else:
                                        usuario_antigo = usuario
                                        senha_antiga = senha
                                        if usuario in bibliotecas:
                                            bibliotecas[novo_usuario] = bibliotecas.pop(usuario_antigo)
                                            usuarios.remove(usuario_antigo)
                                            senhas.remove(senha_antiga)
                                            usuarios.append(novo_usuario)
                                            senhas.append(nova_senha)
                                            usuario = novo_usuario
                                            senha = nova_senha
                                            usuarioCadastrado = novo_usuario
                                            senhaCadastrada = nova_senha
                                            voltando()
                                            print(f"O nome de usuário foi alterado de '{usuario_antigo}' para '{novo_usuario}'.")
                                            time.sleep(2.5)
                                            os.system('cls')
                                            usuario_antigo = None
                                            senha_antiga = None
                                            break
                                        else:
                                            print(f"O usuário '{usuario}' não foi encontrado.")
                            if 1 == 1:
                                break
                        else:
                            os.system('cls')
                            print("Usuario ou senha incorretos, tente novamente!")

                elif (menu == "4"):
                    os.system('cls')
                    print("Até mais", usuario)
                    saindo()
                    break

                else:
                    os.system('cls')
                    print("Você deve escolher uma das opções abaixo, (1-4).")
            # sair para area de cadastro
            if 1 == 1:
                break
        # erro ao entrar em alguma conta
        else:
            print("Usuário ou senha incorretos! Tente novamente!")
            break