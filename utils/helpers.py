# utils/helpers.py
import os
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def aguardar_e_limpar(segundos=1):
    time.sleep(segundos)
    limpar_tela()

def exibir_mensagem_e_aguardar(mensagem, segundos_espera=2, limpar_apos=True):
    # Exibe uma mensagem, aguarda e opcionalmente limpa a tela.
    print(mensagem)
    time.sleep(segundos_espera)
    if limpar_apos:
        limpar_tela()

def sair_da_conta_mensagem():
    # Exibe mensagem de logout.
    print("Saindo da conta...")
    aguardar_e_limpar(1)

def texto_placeholder_livro():
    print()
    texto()
    print(35*"-=")
    print()
    input("Pressione qualquer tecla para voltar...")
    
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