# repositories/repositorio_livros.py
import json
import os
from typing import List, Dict, Optional
from models.livro import Livro

class RepositorioLivros:
    def __init__(self, caminho_arquivo_livros: str = "db/livros.json"):
        self.caminho_arquivo = caminho_arquivo_livros
        self._garantir_arquivo_existente()
        self.catalogo_livros: List[Livro] = self._carregar_livros_do_arquivo()

    def _garantir_arquivo_existente(self):
        """Garante que o diretório e o arquivo de livros existam."""
        os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
        if not os.path.exists(self.caminho_arquivo):
            # Livros iniciais baseados no db/livros.json original
            livros_iniciais_data = [
                {"titulo": "Dom Casmurro", "genero": "Romance"},
                {"titulo": "1984", "genero": "Distopia"},
                {"titulo": "O Pequeno Príncipe", "genero": "Fábula"},
                {"titulo": "Cem Anos de Solidão", "genero": "Realismo Mágico"},
                {"titulo": "A Revolução dos Bichos", "genero": "Política"},
                {"titulo": "O Senhor dos Anéis", "genero": "Fantasia"},
                {"titulo": "Harry Potter e a Pedra Filosofal", "genero": "Fantasia"},
                {"titulo": "Orgulho e Preconceito", "genero": "Romance"},
                {"titulo": "O Hobbit", "genero": "Fantasia"},
                {"titulo": "O Código Da Vinci", "genero": "Suspense"}
            ]
            with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(livros_iniciais_data, f, indent=4, ensure_ascii=False)

    def _carregar_livros_do_arquivo(self) -> List[Livro]:
        """Carrega os livros do arquivo JSON."""
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                livros_data = json.load(f)
                return [Livro.from_dict(data) for data in livros_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return [] # Retorna lista vazia se o arquivo não existir ou for inválido

    def _salvar_livros_no_arquivo(self):
        """Salva a lista atual de livros no arquivo JSON."""
        livros_data = [livro.to_dict() for livro in self.catalogo_livros]
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(livros_data, f, indent=4, ensure_ascii=False)

    def listar_todos(self) -> List[Livro]:
        """Retorna todos os livros do catálogo."""
        return self.catalogo_livros

    def buscar_por_titulo(self, titulo: str) -> Optional[Livro]:
        """Busca um livro pelo título."""
        for livro in self.catalogo_livros:
            if livro.titulo == titulo:
                return livro
        return None

    def adicionar_livro(self, titulo: str, genero: str) -> bool:
        """Adiciona um novo livro ao catálogo. Retorna True se bem-sucedido."""
        if self.buscar_por_titulo(titulo):
            return False  # Livro já existe
        novo_livro = Livro(titulo, genero)
        self.catalogo_livros.append(novo_livro)
        self._salvar_livros_no_arquivo()
        return True

    def atualizar_livro(self, titulo_original: str, novo_titulo: str, novo_genero: str) -> bool:
        """Atualiza um livro existente. Retorna True se bem-sucedido."""
        livro = self.buscar_por_titulo(titulo_original)
        if not livro:
            return False # Livro não encontrado

        # Verifica se o novo título já existe (e não é o próprio livro)
        if novo_titulo != titulo_original and self.buscar_por_titulo(novo_titulo):
            print(f"Erro: Já existe um livro com o título '{novo_titulo}'.")
            return False

        livro.titulo = novo_titulo
        livro.genero = novo_genero
        self._salvar_livros_no_arquivo()
        return True

    def remover_livro_por_titulo(self, titulo: str) -> Optional[Livro]:
        """Remove um livro do catálogo pelo título. Retorna o livro removido ou None."""
        livro_para_remover = self.buscar_por_titulo(titulo)
        if livro_para_remover:
            self.catalogo_livros.remove(livro_para_remover)
            self._salvar_livros_no_arquivo()
            return livro_para_remover
        return None