import unittest
import json
import os
from unittest.mock import patch, mock_open
from models.livro import Livro 
from repositories.repositorio_livros import RepositorioLivros 

class TestRepositorioLivros(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_livros.json" 
        with patch('os.makedirs'), patch('os.path.exists', return_value=True):
            self.repo = RepositorioLivros(self.test_file)
            self.repo.catalogo_livros = []

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('repositories.repositorio_livros.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('os.path.exists', return_value=False)
    @patch('os.makedirs')
    def test_garantir_arquivo_existente_cria_arquivo(self, mock_makedirs, mock_exists, mock_json_dump, mock_file_open):
        """Testa se _garantir_arquivo_existente cria o arquivo e o preenche se ele não existir."""

        self.repo.catalogo_livros = []
        self.repo._garantir_arquivo_existente()
        mock_makedirs.assert_called_once_with(os.path.dirname(self.test_file), exist_ok=True)
        mock_exists.assert_called_once_with(self.test_file)
        mock_file_open.assert_called_once_with(self.test_file, "w", encoding="utf-8")
        mock_json_dump.assert_called_once()
        args, kwargs = mock_json_dump.call_args
        initial_data = args[0]
        self.assertGreater(len(initial_data), 0) 

    @patch('repositories.repositorio_livros.open', new_callable=mock_open, read_data='[{"titulo": "Livro Teste", "genero": "Teste"}]')
    @patch('json.load', return_value=[{"titulo": "Livro Teste", "genero": "Teste"}])
    def test_carregar_livros_do_arquivo(self, mock_json_load, mock_file_open):
        """Testa o carregamento de livros de um arquivo JSON."""
        livros = self.repo._carregar_livros_do_arquivo()
        mock_file_open.assert_called_once_with(self.test_file, "r", encoding="utf-8")
        mock_json_load.assert_called_once()
        self.assertEqual(len(livros), 1)
        self.assertEqual(livros[0].titulo, "Livro Teste")

    @patch('repositories.repositorio_livros.open', new_callable=mock_open)
    @patch('json.dump')
    def test_salvar_livros_no_arquivo(self, mock_json_dump, mock_file_open):
        """Testa o salvamento de livros em um arquivo JSON."""
        self.repo.catalogo_livros = [Livro("Novo Livro", "Ficção")]
        self.repo._salvar_livros_no_arquivo()
        mock_file_open.assert_called_once_with(self.test_file, "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with([{"titulo": "Novo Livro", "genero": "Ficção"}], mock_file_open(), indent=4, ensure_ascii=False)

    def test_listar_todos(self):
        """Testa a listagem de todos os livros no catálogo."""
        livro1 = Livro("Livro A", "Gen A")
        livro2 = Livro("Livro B", "Gen B")
        self.repo.catalogo_livros = [livro1, livro2]
        self.assertEqual(self.repo.listar_todos(), [livro1, livro2])

    def test_buscar_por_titulo(self):
        """Testa a busca de um livro pelo título."""
        livro1 = Livro("Livro A", "Gen A")
        self.repo.catalogo_livros = [livro1]
        self.assertEqual(self.repo.buscar_por_titulo("Livro A"), livro1)
        self.assertIsNone(self.repo.buscar_por_titulo("Livro C"))

    @patch.object(RepositorioLivros, '_salvar_livros_no_arquivo')
    def test_adicionar_livro_sucesso(self, mock_salvar):
        """Testa a adição de um novo livro com sucesso."""
        self.assertTrue(self.repo.adicionar_livro("Novo Livro", "Ficção"))
        self.assertEqual(len(self.repo.catalogo_livros), 1)
        self.assertEqual(self.repo.catalogo_livros[0].titulo, "Novo Livro")
        mock_salvar.assert_called_once()

    @patch.object(RepositorioLivros, '_salvar_livros_no_arquivo')
    def test_adicionar_livro_ja_existe(self, mock_salvar):
        """Testa a tentativa de adicionar um livro que já existe."""
        self.repo.catalogo_livros.append(Livro("Livro Existente", "Gen"))
        self.assertFalse(self.repo.adicionar_livro("Livro Existente", "Gen"))
        self.assertEqual(len(self.repo.catalogo_livros), 1) 
        mock_salvar.assert_not_called()

    @patch.object(RepositorioLivros, '_salvar_livros_no_arquivo')
    def test_atualizar_livro_sucesso(self, mock_salvar):
        """Testa a atualização de um livro existente com sucesso."""
        self.repo.catalogo_livros.append(Livro("Livro Antigo", "Antigo"))
        self.assertTrue(self.repo.atualizar_livro("Livro Antigo", "Livro Novo", "Novo"))
        livro_atualizado = self.repo.buscar_por_titulo("Livro Novo")
        self.assertIsNotNone(livro_atualizado)
        self.assertEqual(livro_atualizado.titulo, "Livro Novo")
        self.assertEqual(livro_atualizado.genero, "Novo")
        mock_salvar.assert_called_once()

    @patch.object(RepositorioLivros, '_salvar_livros_no_arquivo')
    @patch('builtins.print') 
    def test_atualizar_livro_novo_titulo_existe(self, mock_print, mock_salvar):
        """Testa a tentativa de atualizar um livro com um título que já existe (outro livro)."""
        self.repo.catalogo_livros.append(Livro("Livro A", "Gen A"))
        self.repo.catalogo_livros.append(Livro("Livro B", "Gen B"))
        self.assertFalse(self.repo.atualizar_livro("Livro A", "Livro B", "Novo"))
        mock_print.assert_called_with("Erro: Já existe um livro com o título 'Livro B'.")
        mock_salvar.assert_not_called()

    @patch.object(RepositorioLivros, '_salvar_livros_no_arquivo')
    def test_atualizar_livro_nao_encontrado(self, mock_salvar):
        """Testa a tentativa de atualizar um livro que não existe."""
        self.assertFalse(self.repo.atualizar_livro("Livro Inexistente", "Novo", "Novo"))
        mock_salvar.assert_not_called()

    @patch.object(RepositorioLivros, '_salvar_livros_no_arquivo')
    def test_remover_livro_por_titulo_sucesso(self, mock_salvar):
        """Testa a remoção de um livro por título com sucesso."""
        livro_remover = Livro("Para Remover", "R")
        self.repo.catalogo_livros.append(livro_remover)
        removido = self.repo.remover_livro_por_titulo("Para Remover")
        self.assertEqual(removido, livro_remover)
        self.assertNotIn(livro_remover, self.repo.catalogo_livros)
        mock_salvar.assert_called_once()

    @patch.object(RepositorioLivros, '_salvar_livros_no_arquivo')
    def test_remover_livro_por_titulo_nao_encontrado(self, mock_salvar):
        """Testa a tentativa de remover um livro por título que não existe."""
        self.repo.catalogo_livros.append(Livro("Ainda Aqui", "G"))
        removido = self.repo.remover_livro_por_titulo("Nao Existe")
        self.assertIsNone(removido)
        self.assertEqual(len(self.repo.catalogo_livros), 1)
        mock_salvar.assert_not_called()

if __name__ == '__main__':
    unittest.main()