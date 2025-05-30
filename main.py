# main.py
from models.sistema import Sistema

def iniciar_aplicacao():
    """Inicializa e executa o sistema da biblioteca."""
    sistema_biblioteca = Sistema()
    sistema_biblioteca.iniciar_sessao()
    print("Programa encerrado.")

if __name__ == "__main__":
    iniciar_aplicacao()