from models.usuario import Usuario
from models.biblioteca import Biblioteca
from core.defs import carregar_usuarios, salvar_usuarios

class Sistema:
    def __init__(self):
        self.biblioteca = Biblioteca()  # Objeto para gerenciar livros disponíveis
        self._carregar_usuarios()
        print(f"[DEBUG] Usando objeto da classe: {self.__class__}")

    def _carregar_usuarios(self):
        dados = carregar_usuarios()
        self.usuarios = dados.get('usuarios', [])
        self.senhas = dados.get('senhas', {})
        self.bibliotecas = dados.get('bibliotecas', {})

    def _salvar_usuarios(self):
        salvar_usuarios({
            'usuarios': self.usuarios,
            'senhas': self.senhas,
            'bibliotecas': self.bibliotecas
        })

    def atualizar_dados(self):
        """Carrega os dados mais recentes do JSON"""
        self._carregar_usuarios()

    def login(self, usuario, senha):
        self.atualizar_dados()  # Garante os dados mais recentes
        if usuario in self.usuarios and self.senhas.get(usuario) == senha:
            return Usuario(usuario, senha)
        return None

    def cadastro(self, usuario, senha):
        self.atualizar_dados()  # Atualiza antes de cadastrar
        if usuario in self.usuarios:
            return False, "Usuário já existe"
        self.usuarios.append(usuario)
        self.senhas[usuario] = senha
        self.bibliotecas[usuario] = []
        self._salvar_usuarios()
        return True, "Cadastro realizado"

    def mostrar_livros(self):
        for i, livro in enumerate(self.biblioteca.livros, 1):
            print(f"{i} - {livro}")

    def livros_por_genero(self, genero):
        indices = [i for i, livro in enumerate(self.biblioteca.livros) if self.biblioteca.generos[i] == genero]
        for i in indices:
            print(f"{i+1} - {self.biblioteca.livros[i]}")
        return indices

    def adicionar_livro(self, usuario, posicao):
        self.atualizar_dados()  # Sempre atualiza antes de modificar
        livro = self.biblioteca.livros[posicao]
        if usuario in self.bibliotecas:
            if livro not in self.bibliotecas[usuario]:
                self.bibliotecas[usuario].append(livro)
                self._salvar_usuarios()

    def mostrar_biblioteca(self, usuario):
        self.atualizar_dados()
        livros_usuario = self.bibliotecas.get(usuario, [])
        if not livros_usuario:
            print("Sua biblioteca está vazia.")
        else:
            print(f"Biblioteca de {usuario}:")
            for i, livro in enumerate(livros_usuario, 1):
                print(f"{i} - {livro}")

    def remover_livro(self, usuario, posicao):
        self.atualizar_dados()
        livros_usuario = self.bibliotecas.get(usuario, [])
        if 0 <= posicao < len(livros_usuario):
            livro = livros_usuario.pop(posicao)
            self._salvar_usuarios()
            return livro
        return None

    def alterar_usuario(self, usuario_antigo, novo_usuario, nova_senha):
        self.atualizar_dados()
        if novo_usuario in self.usuarios:
            return False, "Usuário já em uso"
        if usuario_antigo not in self.usuarios:
            return False, "Usuário antigo não encontrado"

        self.usuarios.remove(usuario_antigo)
        self.usuarios.append(novo_usuario)

        senha_antiga = self.senhas.pop(usuario_antigo)
        self.senhas[novo_usuario] = nova_senha

        if usuario_antigo in self.bibliotecas:
            self.bibliotecas[novo_usuario] = self.bibliotecas.pop(usuario_antigo)
        else:
            self.bibliotecas[novo_usuario] = []

        self._salvar_usuarios()
        return True, "Usuário alterado com sucesso"
