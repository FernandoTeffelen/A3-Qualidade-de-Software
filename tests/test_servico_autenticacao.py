import unittest
from unittest.mock import patch, MagicMock
from services.autenticacao import ServicoAutenticacao
from repositories.repositorio_usuarios import RepositorioUsuarios

class TestServicoAutenticacao(unittest.TestCase):
    def setUp(self):
        self.mock_repo_usuarios = MagicMock(spec=RepositorioUsuarios)
        self.servico_autenticacao = ServicoAutenticacao(self.mock_repo_usuarios)

    @patch('services.autenticacao.getpass', side_effect=['testpass'])
    @patch('builtins.input', side_effect=['testuser'])
    def test_login_sucesso(self, mock_input, mock_getpass): 
        """Testa o login com credenciais corretas."""
        self.mock_repo_usuarios.buscar_senha.return_value = 'testpass'
        
        resultado = self.servico_autenticacao.login()
        
        mock_input.assert_called_once_with("Usuário: ")
        mock_getpass.assert_called_once_with("Senha: ") 
        self.mock_repo_usuarios.buscar_senha.assert_called_once_with('testuser')
        self.assertEqual(resultado, 'testuser')

    @patch('services.autenticacao.getpass', side_effect=['wrongpass'])
    @patch('builtins.input', side_effect=['testuser'])
    @patch('builtins.print')
    def test_login_falha_senha_incorreta(self, mock_print, mock_input, mock_getpass):
        """Testa o login com senha incorreta."""
        self.mock_repo_usuarios.buscar_senha.return_value = 'correctpass'
        
        resultado = self.servico_autenticacao.login()
        
        mock_input.assert_called_once_with("Usuário: ")
        mock_getpass.assert_called_once_with("Senha: ")
        self.mock_repo_usuarios.buscar_senha.assert_called_once_with('testuser')
        self.assertIsNone(resultado)
        mock_print.assert_called_with("Usuário ou senha incorretos.")

    @patch('services.autenticacao.getpass', side_effect=['anypass'])
    @patch('builtins.input', side_effect=['nonexistentuser'])
    @patch('builtins.print')
    def test_login_falha_usuario_inexistente(self, mock_print, mock_input, mock_getpass):
        """Testa o login com usuário inexistente."""
        self.mock_repo_usuarios.buscar_senha.return_value = None
        
        resultado = self.servico_autenticacao.login()
        
        mock_input.assert_called_once_with("Usuário: ")
        mock_getpass.assert_called_once_with("Senha: ")
        self.mock_repo_usuarios.buscar_senha.assert_called_once_with('nonexistentuser')
        self.assertIsNone(resultado)
        mock_print.assert_called_with("Usuário ou senha incorretos.")


    @patch('services.autenticacao.getpass', side_effect=['newpass', 'newpass'])
    @patch('builtins.input', side_effect=['newuser'])
    @patch('builtins.print')
    def test_cadastro_sucesso(self, mock_print, mock_input, mock_getpass):
        """Testa o cadastro de um novo usuário com sucesso."""
        self.mock_repo_usuarios.existe_usuario.return_value = False
        self.mock_repo_usuarios.adicionar_usuario.return_value = True
        
        resultado = self.servico_autenticacao.cadastro()
        
        mock_input.assert_called_once_with("Escolha um nome de usuário: ")
        mock_getpass.assert_any_call("Escolha uma senha: ")
        mock_getpass.assert_any_call("Confirme a senha: ")
    
        self.assertEqual(mock_getpass.call_count, 2)
        self.mock_repo_usuarios.existe_usuario.assert_called_once_with('newuser')
        self.mock_repo_usuarios.adicionar_usuario.assert_called_once_with('newuser', 'newpass')
        self.assertEqual(resultado, 'newuser')
        mock_print.assert_called_with("Cadastro realizado com sucesso!")

    @patch('builtins.input', side_effect=[''])
    @patch('builtins.print')
    def test_cadastro_falha_nome_vazio(self, mock_print, mock_input):
        """Testa o cadastro com nome de usuário vazio."""
        resultado = self.servico_autenticacao.cadastro()
        self.assertIsNone(resultado)
        mock_input.assert_called_once_with("Escolha um nome de usuário: ")
        mock_print.assert_called_with("Nome de usuário não pode ser vazio.")
        self.mock_repo_usuarios.existe_usuario.assert_not_called()

    @patch('services.autenticacao.getpass', side_effect=['anypass', 'anypass'])
    @patch('builtins.input', side_effect=['existinguser'])
    @patch('builtins.print')
    def test_cadastro_falha_usuario_existente(self, mock_print, mock_input, mock_getpass):
        """Testa o cadastro com nome de usuário já existente."""
        self.mock_repo_usuarios.existe_usuario.return_value = True
        
        resultado = self.servico_autenticacao.cadastro()
        
        mock_input.assert_called_once_with("Escolha um nome de usuário: ")
        self.mock_repo_usuarios.existe_usuario.assert_called_once_with('existinguser')
        mock_print.assert_called_with("Usuário já existe.")
        self.mock_repo_usuarios.adicionar_usuario.assert_not_called()
        mock_getpass.assert_not_called() 


    @patch('services.autenticacao.getpass', side_effect=['', '']) 
    @patch('builtins.input', side_effect=['validuser'])
    @patch('builtins.print')
    def test_cadastro_falha_senha_vazia(self, mock_print, mock_input, mock_getpass):
        """Testa o cadastro com senha vazia."""
        self.mock_repo_usuarios.existe_usuario.return_value = False
        
        resultado = self.servico_autenticacao.cadastro()
        
        mock_input.assert_called_once_with("Escolha um nome de usuário: ")
        mock_getpass.assert_called_once_with("Escolha uma senha: ") 
        mock_print.assert_called_with("Senha não pode ser vazia.")
        self.mock_repo_usuarios.adicionar_usuario.assert_not_called()
        self.assertEqual(mock_getpass.call_count, 1)

    @patch('services.autenticacao.getpass', side_effect=['pass1', 'pass2'])
    @patch('builtins.input', side_effect=['validuser'])
    @patch('builtins.print')
    def test_cadastro_falha_senhas_nao_coincidem(self, mock_print, mock_input, mock_getpass):
        """Testa o cadastro com senhas que não coincidem."""
        self.mock_repo_usuarios.existe_usuario.return_value = False
        
        resultado = self.servico_autenticacao.cadastro()
        
        mock_input.assert_called_once_with("Escolha um nome de usuário: ")
        mock_getpass.assert_any_call("Escolha uma senha: ")
        mock_getpass.assert_any_call("Confirme a senha: ")
        self.assertEqual(mock_getpass.call_count, 2) 
        mock_print.assert_called_with("As senhas não coincidem.")
        self.mock_repo_usuarios.adicionar_usuario.assert_not_called()

    @patch('services.autenticacao.getpass', side_effect=['pass_fail', 'pass_fail'])
    @patch('builtins.input', side_effect=['user_fail_add'])
    @patch('builtins.print')
    def test_cadastro_falha_adicionar_usuario_no_repo(self, mock_print, mock_input, mock_getpass):
        """Testa o cenário onde o repositório falha ao adicionar o usuário."""
        self.mock_repo_usuarios.existe_usuario.return_value = False
        self.mock_repo_usuarios.adicionar_usuario.return_value = False  
        
        resultado = self.servico_autenticacao.cadastro()
        
        mock_input.assert_called_once_with("Escolha um nome de usuário: ")
        mock_getpass.assert_any_call("Escolha uma senha: ")
        mock_getpass.assert_any_call("Confirme a senha: ")
        self.assertEqual(mock_getpass.call_count, 2)
        mock_print.assert_called_with("Falha ao cadastrar. Tente novamente.")
        self.mock_repo_usuarios.adicionar_usuario.assert_called_once_with('user_fail_add', 'pass_fail')

if __name__ == '__main__':
    unittest.main()