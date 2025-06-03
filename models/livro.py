# models/livro.py
class Livro:
    def __init__(self, titulo: str, genero: str):
        # Inicializa um novo objeto Livro.
        self.titulo = titulo
        self.genero = genero

    def __str__(self):
        # Retorna uma representação em string do livro.
        return f"{self.titulo} ({self.genero})"

    def __eq__(self, other):
        #Verifica se este livro é igual a outro, comparando título e gênero.
        if not isinstance(other, Livro):
            return NotImplemented
        return self.titulo == other.titulo and self.genero == other.genero

    def __hash__(self):
        # Retorna um hash para o livro, baseado no título e gênero.
        # Essencial para que objetos Livro possam ser usados em sets e como chaves de dicionários.
        return hash((self.titulo, self.genero))

    def to_dict(self):
        # Converte o objeto Livro para um dicionário.
        return {"titulo": self.titulo, "genero": self.genero}

    @staticmethod
    def from_dict(data: dict):
        #Cria um objeto Livro a partir de um dicionário.
        return Livro(data['titulo'], data['genero'])