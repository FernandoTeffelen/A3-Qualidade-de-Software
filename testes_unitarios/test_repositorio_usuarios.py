import unittest
import json
import os
from unittest.mock import patch, mock_open
from models.livro import Livro 
from repositories.repositorio_usuarios import RepositorioUsuarios

MOCK_INITIAL_USER_DATA = {
    "usuarios": ["admin", "testuser"],
    "senhas": {"admin": "admin", "testuser": "testpass"},
    "bibliotecas": {"admin": [], "testuser": []}
}
MOCK_LIVRO_DATA = {"titulo": "Livro Mock", "genero": "Mock"}
MOCK_TEST_DIR = "temp_test_db" 

class TestRepositorioUsuarios(unittest.TestCase):
    """Conjunto de testes para a classe RepositorioUsuarios."""

    def setUp(self):
        """Configura o ambiente de teste antes de cada teste."""
        self.test_file = os.path.join(MOCK_TEST_DIR, "test_usuarios.json")
        self.patchers = []
        
        self.patch_makedirs = patch('repositories.repositorio_usuarios.os.makedirs')
        self.mock_makedirs = self.patch_makedirs.start()
        self.patchers.append(self.patch_makedirs)
        
        self.patch_json_dump = patch('repositories.repositorio_usuarios.json.dump')
        self.mock_json_dump = self.patch_json_dump.start()
        self.patchers.append(self.patch_json_dump)

    def tearDown(self):
        """Limpa o ambiente de teste após cada teste."""
        for p in self.patchers:
            p.stop()
        
        if os.path.exists(MOCK_TEST_DIR) and os.path.isdir(MOCK_TEST_DIR):
            for filename in os.listdir(MOCK_TEST_DIR):
                file_path = os.path.join(MOCK_TEST_DIR, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(MOCK_TEST_DIR)

    @patch('repositories.repositorio_usuarios.os.path.exists')
    @patch('repositories.repositorio_usuarios.open', new_callable=mock_open)
    @patch('repositories.repositorio_usuarios.json.loads') 
    def test_carregar_dados_do_arquivo_valido(self, mock_json_loads, mock_open_file, mock_exists):
        """Testa o carregamento de dados válidos de um arquivo JSON."""
        mock_exists.return_value = True 
        mock_open_file.return_value.read.return_value = json.dumps(MOCK_INITIAL_USER_DATA)
        mock_json_loads.return_value = MOCK_INITIAL_USER_DATA.copy() 
        
        repo = RepositorioUsuarios(self.test_file) 
        
        mock_exists.assert_called_with(self.test_file) 
        mock_open_file.assert_called_with(self.test_file, "r", encoding="utf-8") 
        self.assertEqual(repo.dados_usuarios, MOCK_INITIAL_USER_DATA)

    @patch('repositories.repositorio_usuarios.os.path.exists')
    @patch('repositories.repositorio_usuarios.open', new_callable=mock_open)
    @patch('repositories.repositorio_usuarios.json.loads') 
    def test_carregar_dados_do_arquivo_inexistente(self, mock_json_loads, mock_open_file, mock_exists):
        """Testa o carregamento quando o arquivo não existe."""
        mock_exists.return_value = False 
        mock_open_file.return_value.read.return_value = '' 
        
        dados_iniciais_esperados = {"usuarios": ["admin"], "senhas": {"admin": "admin"}, "bibliotecas": {"admin": []}}
        
        repo = RepositorioUsuarios(self.test_file) 

        self.mock_json_dump.assert_any_call(
            dados_iniciais_esperados, mock_open_file().__enter__(), indent=4, ensure_ascii=False
        )
        self.assertEqual(self.mock_json_dump.call_count, 2)
        
        mock_exists.assert_called_with(self.test_file) 
        mock_open_file.assert_any_call(self.test_file, "w", encoding="utf-8") 
        mock_open_file.assert_any_call(self.test_file, "r", encoding="utf-8")
        
        mock_json_loads.assert_not_called() 

        self.assertEqual(repo.dados_usuarios, dados_iniciais_esperados)

    def test_salvar_dados_no_arquivo(self):
        """Testa o salvamento de dados no arquivo JSON."""
        with patch('repositories.repositorio_usuarios.open', new_callable=mock_open) as mock_open_file:
            with patch('repositories.repositorio_usuarios.json.loads') as mock_json_loads:
                mock_json_loads.return_value = MOCK_INITIAL_USER_DATA.copy()
                mock_open_file.return_value.read.return_value = json.dumps(MOCK_INITIAL_USER_DATA)
                
                repo = RepositorioUsuarios(self.test_file) 
                
                self.mock_json_dump.reset_mock() 
                mock_open_file.reset_mock() 

                repo.dados_usuarios = MOCK_INITIAL_USER_DATA.copy() 
                repo._salvar_dados_no_arquivo()

                mock_open_file.assert_called_once_with(self.test_file, "w", encoding="utf-8")
                self.mock_json_dump.assert_called_once_with(
                    MOCK_INITIAL_USER_DATA, mock_open_file().__enter__(), indent=4, ensure_ascii=False
                )

    def test_buscar_senha_existe(self):
        """Testa a busca de senha de um usuário existente."""
        with patch('repositories.repositorio_usuarios.os.path.exists') as mock_exists:
            with patch('repositories.repositorio_usuarios.open', new_callable=mock_open) as mock_open_file:
                with patch('repositories.repositorio_usuarios.json.loads') as mock_json_loads:
                    mock_exists.return_value = True
                    mock_open_file.return_value.read.return_value = json.dumps({"usuarios": ["user_test"], "senhas": {"user_test": "pass_test"}, "bibliotecas": {"user_test": []}})
                    mock_json_loads.return_value = {"usuarios": ["user_test"], "senhas": {"user_test": "pass_test"}, "bibliotecas": {"user_test": []}}
                    
                    repo = RepositorioUsuarios(self.test_file)
                    self.assertEqual(repo.buscar_senha('user_test'), 'pass_test')

    def test_adicionar_usuario_sucesso(self):
        """Testa a adição de um novo usuário com sucesso."""
        with patch('repositories.repositorio_usuarios.os.path.exists') as mock_exists:
            with patch('repositories.repositorio_usuarios.open', new_callable=mock_open) as mock_open_file:
                with patch('repositories.repositorio_usuarios.json.loads') as mock_json_loads:
                    mock_exists.return_value = True
                    mock_open_file.return_value.read.return_value = json.dumps({"usuarios": ["admin"], "senhas": {"admin": "admin"}, "bibliotecas": {"admin": []}})
                    mock_json_loads.return_value = {"usuarios": ["admin"], "senhas": {"admin": "admin"}, "bibliotecas": {"admin": []}}
                    
                    repo = RepositorioUsuarios(self.test_file)
                    self.mock_json_dump.reset_mock() 
                    
                    result = repo.adicionar_usuario('novo_user', 'nova_senha')
                    self.assertTrue(result)
                    self.assertIn('novo_user', repo.dados_usuarios['usuarios'])
                    self.assertEqual(repo.dados_usuarios['senhas']['novo_user'], 'nova_senha')
                    self.mock_json_dump.assert_called_once()

    def test_remover_usuario_sucesso(self):
        """Testa a remoção de um usuário com sucesso."""
        with patch('repositories.repositorio_usuarios.os.path.exists') as mock_exists:
            with patch('repositories.repositorio_usuarios.open', new_callable=mock_open) as mock_open_file:
                with patch('repositories.repositorio_usuarios.json.loads') as mock_json_loads:
                    mock_exists.return_value = True
                    mock_open_file.return_value.read.return_value = json.dumps({"usuarios": ["admin", "user_to_remove"], "senhas": {"admin": "admin", "user_to_remove": "pass"}, "bibliotecas": {"admin": [], "user_to_remove": []}})
                    mock_json_loads.return_value = {"usuarios": ["admin", "user_to_remove"], "senhas": {"admin": "admin", "user_to_remove": "pass"}, "bibliotecas": {"admin": [], "user_to_remove": []}}
                    
                    repo = RepositorioUsuarios(self.test_file)
                    self.mock_json_dump.reset_mock() 
                    
                    result = repo.remover_usuario('user_to_remove')
                    self.assertTrue(result)
                    self.assertNotIn('user_to_remove', repo.dados_usuarios['usuarios'])
                    self.mock_json_dump.assert_called_once()

    def test_alterar_dados_usuario_sucesso(self):
        """Testa a alteração de nome e senha de um usuário."""
        with patch('repositories.repositorio_usuarios.os.path.exists') as mock_exists:
            with patch('repositories.repositorio_usuarios.open', new_callable=mock_open) as mock_open_file:
                with patch('repositories.repositorio_usuarios.json.loads') as mock_json_loads:
                    mock_exists.return_value = True
                    mock_open_file.return_value.read.return_value = json.dumps({"usuarios": ["old_user"], "senhas": {"old_user": "old_pass"}, "bibliotecas": {"old_user": []}})
                    mock_json_loads.return_value = {"usuarios": ["old_user"], "senhas": {"old_user": "old_pass"}, "bibliotecas": {"old_user": []}}
                    
                    repo = RepositorioUsuarios(self.test_file)
                    self.mock_json_dump.reset_mock() 
                    
                    sucesso, msg = repo.alterar_dados_usuario('old_user', 'new_user', 'new_pass')
                    self.assertTrue(sucesso)
                    
                    self.assertNotIn('old_user', repo.dados_usuarios['usuarios']) 
                    self.assertIn('new_user', repo.dados_usuarios['usuarios']) 
                    
                    self.assertEqual(repo.dados_usuarios['senhas']['old_user'], 'new_pass') 
                    self.assertEqual(repo.dados_usuarios['senhas']['new_user'], 'old_pass') 
                    
                    self.mock_json_dump.assert_called_once()

    def test_obter_biblioteca_usuario(self):
        """Testa a obtenção da biblioteca de um usuário."""
        with patch('repositories.repositorio_usuarios.os.path.exists') as mock_exists:
            with patch('repositories.repositorio_usuarios.open', new_callable=mock_open) as mock_open_file:
                with patch('repositories.repositorio_usuarios.json.loads') as mock_json_loads:
                    mock_exists.return_value = True
                    mock_open_file.return_value.read.return_value = json.dumps({
                        "usuarios": ["testuser"], 
                        "senhas": {"testuser": "testpass"}, 
                        "bibliotecas": {"testuser": [MOCK_LIVRO_DATA]}
                    })
                    mock_json_loads.return_value = {
                        "usuarios": ["testuser"], 
                        "senhas": {"testuser": "testpass"}, 
                        "bibliotecas": {"testuser": [MOCK_LIVRO_DATA]} 
                    }
                    repo = RepositorioUsuarios(self.test_file)
                    biblioteca = repo.obter_biblioteca_usuario('testuser')
                    self.assertEqual(len(biblioteca), 1)
                    self.assertEqual(biblioteca[0].titulo, "Livro Mock")

    def test_adicionar_livro_na_biblioteca_usuario_sucesso(self):
        """Testa a adição de um livro à biblioteca de um usuário."""
        with patch('repositories.repositorio_usuarios.os.path.exists') as mock_exists:
            with patch('repositories.repositorio_usuarios.open', new_callable=mock_open) as mock_open_file:
                with patch('repositories.repositorio_usuarios.json.loads') as mock_json_loads:
                    mock_exists.return_value = True
                    mock_open_file.return_value.read.return_value = json.dumps({"usuarios": ["user_lib"], "senhas": {"user_lib": "pass"}, "bibliotecas": {"user_lib": []}})
                    mock_json_loads.return_value = {"usuarios": ["user_lib"], "senhas": {"user_lib": "pass"}, "bibliotecas": {"user_lib": []}}
                    
                    repo = RepositorioUsuarios(self.test_file)
                    self.mock_json_dump.reset_mock() 
                    
                    livro = Livro("Novo Livro", "Aventura")
                    result = repo.adicionar_livro_na_biblioteca_usuario('user_lib', livro)
                    self.assertTrue(result)
                    self.assertEqual(len(repo.dados_usuarios['bibliotecas']['user_lib']), 1)
                    self.assertEqual(repo.dados_usuarios['bibliotecas']['user_lib'][0], livro.to_dict())
                    self.mock_json_dump.assert_called_once()

    def test_remover_livro_da_biblioteca_usuario_sucesso(self):
        """Testa a remoção de um livro da biblioteca de um usuário."""
        with patch('repositories.repositorio_usuarios.os.path.exists') as mock_exists:
            with patch('repositories.repositorio_usuarios.open', new_callable=mock_open) as mock_open_file:
                with patch('repositories.repositorio_usuarios.json.loads') as mock_json_loads:
                    mock_exists.return_value = True
                    mock_open_file.return_value.read.return_value = json.dumps({"usuarios": ["user_lib"], "senhas": {"user_lib": "pass"}, "bibliotecas": {"user_lib": [MOCK_LIVRO_DATA]}})
                    mock_json_loads.return_value = {"usuarios": ["user_lib"], "senhas": {"user_lib": "pass"}, "bibliotecas": {"user_lib": [MOCK_LIVRO_DATA]}}
                    
                    repo = RepositorioUsuarios(self.test_file)
                    self.mock_json_dump.reset_mock() 
                    
                    removido = repo.remover_livro_da_biblioteca_usuario('user_lib', "Livro Mock")
                    self.assertIsNotNone(removido)
                    self.assertEqual(removido.titulo, "Livro Mock")
                    self.assertEqual(len(repo.dados_usuarios['bibliotecas']['user_lib']), 0)
                    self.mock_json_dump.assert_called_once()

if __name__ == '__main__':
    unittest.main()