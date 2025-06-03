# repositories/repositorio_usuarios.py
import json
import os
from typing import Dict, List, Optional, Tuple
from models.livro import Livro # Para type hinting da biblioteca do usuário

class RepositorioUsuarios:
    def __init__(self, caminho_arquivo_usuarios: str = "db/usuarios.json"):
        # Inicializa o repositório de usuários.
        self.caminho_arquivo = caminho_arquivo_usuarios
        self._garantir_arquivo_existente()
        self.dados_usuarios: Dict = self._carregar_dados_do_arquivo()

    def _garantir_arquivo_existente(self):
        # Garante que o diretório e o arquivo de usuários existam. Cria com dados iniciais (admin) se não existir.
        os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
        if not os.path.exists(self.caminho_arquivo):
            # Estrutura inicial com usuário admin
            dados_iniciais = {
                "usuarios": ["admin"],
                "senhas": {"admin": "admin"}, # Senha padrão para o admin
                "bibliotecas": {"admin": []} # Biblioteca vazia para o admin
            }
            self._salvar_dados_no_arquivo(dados_iniciais)

    def _carregar_dados_do_arquivo(self) -> Dict:
        # Carrega os dados dos usuários do arquivo JSON, garantindo a estrutura e o admin.
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read().strip()
                if not conteudo: # Arquivo vazio
                    # Retorna e salva a estrutura inicial com admin
                    dados_iniciais = {"usuarios": ["admin"], "senhas": {"admin": "admin"}, "bibliotecas": {"admin": []}}
                    self._salvar_dados_no_arquivo(dados_iniciais)
                    return dados_iniciais
                
                dados = json.loads(conteudo)
                
                # Garante que as chaves principais existam
                dados.setdefault("usuarios", [])
                dados.setdefault("senhas", {})
                dados.setdefault("bibliotecas", {})

                # Garante que o usuário admin exista com dados padrão se necessário
                if "admin" not in dados["usuarios"]:
                    dados["usuarios"].append("admin")
                if "admin" not in dados["senhas"]:
                    dados["senhas"]["admin"] = "admin" # Senha padrão
                if "admin" not in dados["bibliotecas"]:
                    dados["bibliotecas"]["admin"] = []

                # Validação e correção de formato da biblioteca (se necessário)
                # Esta parte garante que os livros na biblioteca de cada usuário sejam dicionários
                for nome_usuario, biblioteca_data in dados["bibliotecas"].items():
                    biblioteca_corrigida = []
                    if isinstance(biblioteca_data, list):
                        for item_livro in biblioteca_data:
                            if isinstance(item_livro, dict) and "titulo" in item_livro and "genero" in item_livro:
                                biblioteca_corrigida.append(item_livro)
                            # Adicionar aqui lógica para lidar com formatos antigos se houver
                            # elif isinstance(item_livro, str): # Exemplo de formato antigo
                            #     biblioteca_corrigida.append({"titulo": item_livro, "genero": "Desconhecido"})
                    dados["bibliotecas"][nome_usuario] = biblioteca_corrigida
                return dados
        except (FileNotFoundError, json.JSONDecodeError):
            # Em caso de erro de leitura ou arquivo não encontrado, cria um novo com o admin
            dados_iniciais = {"usuarios": ["admin"], "senhas": {"admin": "admin"}, "bibliotecas": {"admin": []}}
            self._salvar_dados_no_arquivo(dados_iniciais)
            return dados_iniciais

    def _salvar_dados_no_arquivo(self, dados: Optional[Dict] = None):
        # Salva os dados dos usuários (fornecidos ou os atuais) no arquivo JSON.
        dados_para_salvar = dados if dados is not None else self.dados_usuarios
        with open(self.caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)

    def buscar_senha(self, nome_usuario: str) -> Optional[str]:
        # Retorna a senha de um usuário, se existir.
        return self.dados_usuarios.get("senhas", {}).get(nome_usuario)

    def existe_usuario(self, nome_usuario: str) -> bool:
        # Verifica se um usuário com o nome fornecido existe.
        return nome_usuario in self.dados_usuarios.get("usuarios", [])

    def adicionar_usuario(self, nome_usuario: str, senha: str) -> bool:
        # Adiciona um novo usuário. Retorna True se bem-sucedido, False se o usuário já existe.
        if self.existe_usuario(nome_usuario):
            return False # Usuário já existe
        
        self.dados_usuarios.setdefault("usuarios", []).append(nome_usuario)
        self.dados_usuarios.setdefault("senhas", {})[nome_usuario] = senha
        self.dados_usuarios.setdefault("bibliotecas", {})[nome_usuario] = [] # Biblioteca inicial vazia
        self._salvar_dados_no_arquivo()
        return True

    def remover_usuario(self, nome_usuario: str) -> bool:
        # Remove um usuário. Não permite remover 'admin'. Retorna True se bem-sucedido.
        if nome_usuario == "admin":
            # print("Não é permitido remover o usuário admin.")
            return False
        if not self.existe_usuario(nome_usuario):
            return False # Usuário não encontrado
        
        if nome_usuario in self.dados_usuarios.get("usuarios", []):
            self.dados_usuarios["usuarios"].remove(nome_usuario)
        self.dados_usuarios.get("senhas", {}).pop(nome_usuario, None)
        self.dados_usuarios.get("bibliotecas", {}).pop(nome_usuario, None)
        self._salvar_dados_no_arquivo()
        return True

    def alterar_dados_usuario(self, nome_antigo: str, novo_nome: Optional[str], nova_senha: Optional[str]) -> Tuple[bool, str]:
        # Altera nome de usuário e/ou senha.
        if not self.existe_usuario(nome_antigo):
            return False, "Usuário a ser alterado não encontrado."

        nome_para_atualizar_senha = nome_antigo # Nome a ser usado para atualizar a senha, caso o nome não mude

        if novo_nome and novo_nome != nome_antigo:
            if self.existe_usuario(novo_nome):
                return False, f"O novo nome de usuário '{novo_nome}' já está em uso."
            if nome_antigo == "admin" and novo_nome != "admin": # Impede renomear o admin para outro nome
                 return False, "Não é permitido renomear o usuário 'admin'."

            # Atualiza o nome na lista de usuários
            try:
                idx = self.dados_usuarios["usuarios"].index(nome_antigo)
                self.dados_usuarios["usuarios"][idx] = novo_nome
            except ValueError:
                return False, "Erro interno ao tentar renomear usuário na lista." # Pouco provável se existe_usuario passou

            # Move os dados de senha e biblioteca para o novo nome
            if nome_antigo in self.dados_usuarios["senhas"]:
                self.dados_usuarios["senhas"][novo_nome] = self.dados_usuarios["senhas"].pop(nome_antigo)
            if nome_antigo in self.dados_usuarios["bibliotecas"]:
                 self.dados_usuarios["bibliotecas"][novo_nome] = self.dados_usuarios["bibliotecas"].pop(nome_antigo)
            
            nome_para_atualizar_senha = novo_nome # O nome mudou, usa o novo nome para a senha
        
        if nova_senha:
            self.dados_usuarios["senhas"][nome_para_atualizar_senha] = nova_senha
        
        self._salvar_dados_no_arquivo()
        return True, "Dados do usuário alterados com sucesso."


    def obter_biblioteca_usuario(self, nome_usuario: str) -> List[Livro]:
        # Retorna a lista de objetos Livro da biblioteca de um usuário.
        livros_data = self.dados_usuarios.get("bibliotecas", {}).get(nome_usuario, [])
        return [Livro.from_dict(data) for data in livros_data if isinstance(data, dict)]

    def adicionar_livro_na_biblioteca_usuario(self, nome_usuario: str, livro: Livro) -> bool:
        # Adiciona um livro (objeto Livro) à biblioteca de um usuário. Retorna True se bem-sucedido.
        if not self.existe_usuario(nome_usuario):
            return False # Usuário não encontrado
        
        biblioteca_usuario_data = self.dados_usuarios.get("bibliotecas", {}).get(nome_usuario, [])
        
        # Verifica se o livro (pelo título) já existe na biblioteca do usuário
        if any(l_data.get("titulo") == livro.titulo for l_data in biblioteca_usuario_data if isinstance(l_data, dict)):
            return False # Livro já existe na biblioteca

        biblioteca_usuario_data.append(livro.to_dict())
        self.dados_usuarios["bibliotecas"][nome_usuario] = biblioteca_usuario_data
        self._salvar_dados_no_arquivo()
        return True

    def remover_livro_da_biblioteca_usuario(self, nome_usuario: str, titulo_livro: str) -> Optional[Livro]:
        # Remove um livro da biblioteca de um usuário pelo título. Retorna o objeto Livro removido ou None.
        if not self.existe_usuario(nome_usuario):
            return None # Usuário não encontrado
        
        biblioteca_usuario_data = self.dados_usuarios.get("bibliotecas", {}).get(nome_usuario, [])
        livro_removido_obj = None
        
        nova_biblioteca_data = []
        for livro_data in biblioteca_usuario_data:
            if isinstance(livro_data, dict) and livro_data.get("titulo") == titulo_livro:
                livro_removido_obj = Livro.from_dict(livro_data) # Guarda para retornar
            else:
                nova_biblioteca_data.append(livro_data)
        
        if livro_removido_obj: # Se um livro foi efetivamente marcado para remoção
            self.dados_usuarios["bibliotecas"][nome_usuario] = nova_biblioteca_data
            self._salvar_dados_no_arquivo()
            return livro_removido_obj
        return None # Livro não encontrado na biblioteca

    def listar_todos_nomes_usuarios(self, incluir_admin=True) -> List[str]:
        # Retorna uma lista com os nomes de todos os usuários.
        todos_usuarios = list(self.dados_usuarios.get("usuarios", []))
        if incluir_admin:
            return todos_usuarios
        else:
            return [u for u in todos_usuarios if u != "admin"]
