class Livro:
    def __init__(self, titulo, genero):
        print(f"[DEBUG] Usando objeto da classe: {self.__class__}")
        self.titulo = titulo
        self.genero = genero
