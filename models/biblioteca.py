class Biblioteca:
    def __init__(self):
        self.usuarios = ['admin']
        self.senhas = ['admin']
        self.bibliotecas = {'admin': []}

    def usuario_existe(self, nome):
        return nome in self.usuarios

    def cadastrar_usuario(self, nome, senha):
        self.usuarios.append(nome)
        self.senhas.append(senha)
        self.bibliotecas[nome] = []

    def autenticar(self, nome, senha):
        return nome in self.usuarios and self.senhas[self.usuarios.index(nome)] == senha

    def adicionar_livro_usuario(self, nome, livro):
        if livro in self.bibliotecas[nome]:
            return False
        self.bibliotecas[nome].append(livro)
        return True

    def livros_do_usuario(self, nome):
        return self.bibliotecas.get(nome, [])
