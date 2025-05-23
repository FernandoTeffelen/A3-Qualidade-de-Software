class Usuario:
    def __init__(self, nome, senha):
        print(f"[DEBUG] Usando objeto da classe: {self.__class__}")
        self.nome = nome
        self.senha = senha
