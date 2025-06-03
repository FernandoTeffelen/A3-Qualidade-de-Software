import unittest
from models.livro import Livro 

class TestLivro(unittest.TestCase):
    def test_init(self):
        """Testa a inicialização do objeto Livro."""
        livro = Livro("O Pequeno Príncipe", "Fábula")
        self.assertEqual(livro.titulo, "O Pequeno Príncipe")
        self.assertEqual(livro.genero, "Fábula")

    def test_str(self):
        """Testa a representação em string do objeto Livro."""
        livro = Livro("1984", "Distopia")
        self.assertEqual(str(livro), "1984 (Distopia)")

    def test_eq(self):
        """Testa a comparação de igualdade entre objetos Livro."""
        livro1 = Livro("Dom Casmurro", "Romance")
        livro2 = Livro("Dom Casmurro", "Romance")
        livro3 = Livro("A Revolução dos Bichos", "Política")

        self.assertEqual(livro1, livro2)
        self.assertNotEqual(livro1, livro3)
        self.assertNotEqual(livro1, "string qualquer") 

    def test_hash(self):
        """Testa a função hash para objetos Livro."""
        livro1 = Livro("Dom Casmurro", "Romance")
        livro2 = Livro("Dom Casmurro", "Romance")
        livro3 = Livro("A Revolução dos Bichos", "Política")

        self.assertEqual(hash(livro1), hash(livro2))
        self.assertNotEqual(hash(livro1), hash(livro3))

    def test_to_dict(self):
        """Testa a conversão do objeto Livro para dicionário."""
        livro = Livro("O Senhor dos Anéis", "Fantasia")
        expected_dict = {"titulo": "O Senhor dos Anéis", "genero": "Fantasia"}
        self.assertEqual(livro.to_dict(), expected_dict)

    def test_from_dict(self):
        """Testa a criação de um objeto Livro a partir de um dicionário."""
        data = {"titulo": "Harry Potter", "genero": "Fantasia"}
        livro = Livro.from_dict(data)
        self.assertIsInstance(livro, Livro)
        self.assertEqual(livro.titulo, "Harry Potter")
        self.assertEqual(livro.genero, "Fantasia")

if __name__ == '__main__':
    unittest.main()