# models/sistema.py
from models.usuario import Usuario
from models.biblioteca import Biblioteca
import json
import os

class Sistema:
    def __init__(self):
        self.usuarios = []            # lista de nomes de usuários (strings)
        self.senhas = {}              # dict {usuario: senha}
        self.bibliotecas = {}         # dict {usuario: [lista de livros]}
        self.biblioteca = Biblioteca()  # objeto Biblioteca para gerenciar livros disponíveis
        print(f"[DEBUG] Usando objeto da classe: {self.__class__}")
        self.carregar_usuarios()

    def carregar_usuarios(self):
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.usuarios = dados.get("usuarios", [])
                self.senhas = dados.get("senhas", {})
                self.bibliotecas = dados.get("bibliotecas", {})

    def salvar_usuarios(self):
        with open("usuarios.json", "w", encoding="utf-8") as f:
            json.dump({
                "usuarios": self.usuarios,
                "senhas": self.senhas,
                "bibliotecas": self.bibliotecas
            }, f, indent=2)

    def login(self, usuario, senha):
        if usuario in self.usuarios and self.senhas.get(usuario) == senha:
            return Usuario(usuario, senha)
        return None

    def cadastro(self, usuario, senha):
        if usuario in self.usuarios:
            return False, "Usuário já existe"
        self.usuarios.append(usuario)
        self.senhas[usuario] = senha
        self.bibliotecas[usuario] = []
        self.salvar_usuarios()
        return True, "Cadastro realizado"

    def mostrar_livros(self):
        # Exibe todos os livros disponíveis da Biblioteca
        for i, livro in enumerate(self.biblioteca.livros, 1):
            print(f"{i} - {livro}")

    def livros_por_genero(self, genero):
        # Retorna lista de índices dos livros do gênero informado
        indices = [i for i, livro in enumerate(self.biblioteca.livros) if self.biblioteca.generos[i] == genero]
        for i in indices:
            print(f"{i+1} - {self.biblioteca.livros[i]}")
        return indices

    def adicionar_livro(self, usuario, posicao):
        livro = self.biblioteca.livros[posicao]
        if usuario in self.bibliotecas:
            if livro not in self.bibliotecas[usuario]:
                self.bibliotecas[usuario].append(livro)
                self.salvar_usuarios()

    def mostrar_biblioteca(self, usuario):
        livros_usuario = self.bibliotecas.get(usuario, [])
        if not livros_usuario:
            print("Sua biblioteca está vazia.")
        else:
            print(f"Biblioteca de {usuario}:")
            for i, livro in enumerate(livros_usuario, 1):
                print(f"{i} - {livro}")

    def remover_livro(self, usuario, posicao):
        livros_usuario = self.bibliotecas.get(usuario, [])
        if 0 <= posicao < len(livros_usuario):
            livro = livros_usuario.pop(posicao)
            self.salvar_usuarios()
            return livro
        return None

    def alterar_usuario(self, usuario_antigo, novo_usuario, nova_senha):
        if novo_usuario in self.usuarios:
            return False, "Usuário já em uso"
        if usuario_antigo not in self.usuarios:
            return False, "Usuário antigo não encontrado"

        # Atualiza usuários
        self.usuarios.remove(usuario_antigo)
        self.usuarios.append(novo_usuario)

        # Atualiza senhas
        senha_antiga = self.senhas.pop(usuario_antigo)
        self.senhas[novo_usuario] = nova_senha

        # Atualiza biblioteca do usuário
        if usuario_antigo in self.bibliotecas:
            self.bibliotecas[novo_usuario] = self.bibliotecas.pop(usuario_antigo)
        else:
            self.bibliotecas[novo_usuario] = []

        self.salvar_usuarios()
        return True, "Usuário alterado com sucesso"
