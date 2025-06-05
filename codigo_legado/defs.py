import os
import time

# arrays
usuarios = ['admin']
senhas = ['admin']
livros = []
generos = []
bibliotecaUsuario = []
bibliotecas = {}

# variaveis
usuario = ''
senha = ''
livro = ''
genero = ''


# DEFinição, para mostrar TODOS os livros cadastrados
def mostrar_livros():
    if (not livros):
        print("Não há nenhum livro cadastrado.\n")
    else:
        print("Lista de livros cadastrados:")
        for i in range(len(livros)):
            print(f"{i + 1} - {livros[i]} - {generos[i]}")


def adicionar_livro(usuario, posicao):
    if usuario not in bibliotecas:
        bibliotecas[usuario] = []  # Se o usuário não tem biblioteca, cria uma lista vazia
    
    # Verifica se o livro já está na biblioteca do usuário
    if livros[posicao] in bibliotecas[usuario]:
        print("Este livro ja pertence a sua bibliotéca.")
    else:
        # Adiciona o livro na posição indicada
        bibliotecas[usuario].append(livros[posicao])


def biblioteca_usuario(usuario):
    if not bibliotecas[usuario]:  # Verifica se a biblioteca do usuário está vazia
        print("Não há nenhum livro na sua biblioteca.\n")
        input("Aperte qualquer tecla para voltar para o menu.")
        os.system('cls')
    else:
        print("Seus livros salvos:")
        for i, livro in enumerate(bibliotecas[usuario], 1):
            print(f"{i} - {livro}\n")
    

def livros_por_genero(genero):
    os.system('cls')
    posicoes = []
    print(f"Livros no gênero '{genero}':")
    for i in range(len(livros)):
        if generos[i].lower() == genero.lower():  # Verifica o gênero
            print(f"{i + 1} - {livros[i]}")
            posicoes.append(i)
    return posicoes


def mostra_usuarios():
    if len(usuarios) <= 1 or not usuarios[1]:  # Verifica se a biblioteca do usuário está vazia
        print("Não há nenhum usuário cadastrado.\n")
        input("Aperte qualquer tecla para voltar para o menu.")
        os.system('cls')
    else:
        print("Usuários cadastrados:")
        for i, usuario in enumerate(usuarios[1:], 2):
            print(f"{i - 1} - {usuario}")


def lorem():
    print("     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.")
    print("Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
    print("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
    print("Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
    
    
def texto():
    lorem()
    lorem()
    print()
    lorem()
    lorem()
    lorem()


def voltando():
    os.system('cls')
    print('Voltando', end='\r')
    time.sleep(0.5)
    print('Voltando.', end='\r')
    time.sleep(0.5)
    print('Voltando..', end='\r')
    time.sleep(0.5)
    print('Voltando...')
    time.sleep(1)
    os.system('cls')


def saindo():
    i = 0
    while i < 2:
        print('Saindo', end='\r')
        time.sleep(0.5)
        print('Saindo.', end='\r')
        time.sleep(0.5)
        print('Saindo..', end='\r')
        time.sleep(0.5)
        print('Saindo...')
        time.sleep(1)
        os.system('cls')
        i += 1
    time.sleep(1)
    os.system('cls')