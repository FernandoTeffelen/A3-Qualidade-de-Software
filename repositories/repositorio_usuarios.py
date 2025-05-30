# repositories/repositorio_usuarios.py
import json
import os
from typing import Dict, List, Optional, Tuple
from models.livro import Livro # Para type hinting da biblioteca do usuário

class RepositorioUsuarios:
    def __init__(self, caminho_arquivo_usuarios: str = "db/usuarios.json"):
        self.caminho_arquivo = caminho_arquivo_usuarios
        self._garantir_arquivo_existente()
        # Estrutura interna: {'usuarios': ['nome1', 'admin'], 'senhas': {'nome1': 's1', 'admin': 'admin'}, 'bibliotecas': {'nome1': [{'titulo': 't', 'genero': 'g'}]}}
        self.dados_usuarios: Dict = self._carregar_dados_do_arquivo()

    def _garantir_arquivo_existente(self):
        """Garante que o diretório e o arquivo de usuários existam."""
        os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
        if not os.path.exists(self.caminho_arquivo):
            # Estrutura inicial com usuário admin
            dados_iniciais = {
                "usuarios": ["admin"],
                "senhas": {"admin": "admin"},
                "bibliotecas": {"admin": []}
            }
            self._salvar_dados_no_arquivo(dados_iniciais)

    def _carregar_dados_do_arquivo(self) -> Dict:
        """Carrega os dados dos usuários do arquivo JSON."""
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read().strip()
                if not conteudo: # Arquivo vazio, inicializa com admin
                    dados_iniciais = {"usuarios": ["admin"], "senhas": {"admin": "admin"}, "bibliotecas": {"admin": []}}
                    self._salvar_dados_no_arquivo(dados_iniciais)
                    return dados_iniciais
                
                dados = json.loads(conteudo)
                # Garante que a estrutura básica exista e que o admin esteja presente
                if "usuarios" not in dados: dados["usuarios"] = []
                if "senhas" not in dados: dados["senhas"] = {}
                if "bibliotecas" not in dados: dados["bibliotecas"] = {}

                if "admin" not in dados["usuarios"]:
                    dados["usuarios"].append("admin")
                    dados["senhas"]["admin"] = "admin" # Senha padrão, se não existir
                    dados["bibliotecas"]["admin"] = dados["bibliotecas"].get("admin", [])
                
                # Converte livros em string (legado) para dicts de Livro.to_dict()
                # Esta parte é crucial para compatibilidade se dados antigos existirem.
                # No entanto, o ideal é que o RepositorioLivros seja a fonte da verdade sobre os livros.
                # Para simplificar aqui, vamos assumir que os livros já estão como dicts.
                # Uma conversão mais robusta buscaria no RepositorioLivros.
                for nome_usuario, livros_serializados in dados["bibliotecas"].items():
                    biblioteca_corrigida = []
                    for item_livro in livros_serializados:
                        if isinstance(item_livro, str): # Formato antigo, apenas título
                            # Idealmente, buscaria o objeto Livro completo no catálogo
                            # print(f"Aviso: Livro '{item_livro}' em formato antigo para usuário '{nome_usuario}'. Será mantido como string por ora.")
                            # Para manter simples, vamos apenas adicionar como um dict com título
                            # Isso pode precisar de ajuste dependendo de como os livros são tratados
                            biblioteca_corrigida.append({"titulo": item_livro, "genero": "Desconhecido"})
                        elif isinstance(item_livro, dict) and "titulo" in item_livro and "genero" in item_livro:
                            biblioteca_corrigida.append(item_livro)
                    dados["bibliotecas"][nome_usuario] = biblioteca_corrigida
                return dados
        except (FileNotFoundError, json.JSONDecodeError):
            # Em caso de erro, retorna uma estrutura padrão com admin
            dados_iniciais = {"usuarios": ["admin"], "senhas": {"admin": "admin"}, "bibliotecas": {"admin": []}}
            self._salvar_dados_no_arquivo(dados_iniciais) # Cria o arquivo com o admin
            return dados_iniciais

    def _salvar_dados_no_arquivo(self, dados: Optional[Dict] = None):
        """Salva os dados dos usuários no arquivo JSON."""
        dados_para_salvar = dados if dados is not None else self.dados_usuarios
        with open(self.caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)

    def buscar_senha(self, nome_usuario: str) -> Optional[str]:
        """Retorna a senha de um usuário."""
        return self.dados_usuarios['senhas'].get(nome_usuario)

    def existe_usuario(self, nome_usuario: str) -> bool:
        """Verifica se um usuário existe."""
        return nome_usuario in self.dados_usuarios['usuarios']

    def adicionar_usuario(self, nome_usuario: str, senha: str) -> bool:
        """Adiciona um novo usuário. Retorna True se bem-sucedido."""
        if self.existe_usuario(nome_usuario):
            return False
        self.dados_usuarios['usuarios'].append(nome_usuario)
        self.dados_usuarios['senhas'][nome_usuario] = senha
        self.dados_usuarios['bibliotecas'][nome_usuario] = []
        self._salvar_dados_no_arquivo()
        return True

    def remover_usuario(self, nome_usuario: str) -> bool:
        """Remove um usuário. Retorna True se bem-sucedido."""
        if nome_usuario == "admin": # Não permite remover admin
            return False
        if not self.existe_usuario(nome_usuario):
            return False
        
        self.dados_usuarios['usuarios'].remove(nome_usuario)
        self.dados_usuarios['senhas'].pop(nome_usuario, None)
        self.dados_usuarios['bibliotecas'].pop(nome_usuario, None)
        self._salvar_dados_no_arquivo()
        return True

    def alterar_dados_usuario(self, nome_antigo: str, novo_nome: Optional[str], nova_senha: Optional[str]) -> Tuple[bool, str]:
        """Altera nome e/ou senha do usuário."""
        if not self.existe_usuario(nome_antigo):
            return False, "Usuário antigo não encontrado."

        nome_final = novo_nome if novo_nome else nome_antigo
        
        if novo_nome and novo_nome != nome_antigo:
            if self.existe_usuario(novo_nome):
                return False, f"Novo nome de usuário '{novo_nome}' já está em uso."
            # Renomear usuário
            idx = self.dados_usuarios['usuarios'].index(nome_antigo)
            self.dados_usuarios['usuarios'][idx] = novo_nome
            
            self.dados_usuarios['senhas'][novo_nome] = self.dados_usuarios['senhas'].pop(nome_antigo)
            self.dados_usuarios['bibliotecas'][novo_nome] = self.dados_usuarios['bibliotecas'].pop(nome_antigo, [])
        
        if nova_senha:
            self.dados_usuarios['senhas'][nome_final] = nova_senha
        
        self._salvar_dados_no_arquivo()
        return True, "Dados do usuário alterados com sucesso."


    def obter_biblioteca_usuario(self, nome_usuario: str) -> List[Livro]:
        """Retorna a lista de Livros da biblioteca de um usuário."""
        livros_data = self.dados_usuarios['bibliotecas'].get(nome_usuario, [])
        return [Livro.from_dict(data) for data in livros_data]

    def adicionar_livro_na_biblioteca_usuario(self, nome_usuario: str, livro: Livro) -> bool:
        """Adiciona um livro à biblioteca de um usuário. Retorna True se bem-sucedido."""
        if not self.existe_usuario(nome_usuario):
            return False
        
        biblioteca_atual_data = self.dados_usuarios['bibliotecas'].get(nome_usuario, [])
        # Evita duplicatas pelo título do livro
        if not any(l['titulo'] == livro.titulo for l in biblioteca_atual_data):
            biblioteca_atual_data.append(livro.to_dict())
            self.dados_usuarios['bibliotecas'][nome_usuario] = biblioteca_atual_data
            self._salvar_dados_no_arquivo()
            return True
        return False # Livro já existe ou usuário não encontrado

    def remover_livro_da_biblioteca_usuario(self, nome_usuario: str, titulo_livro: str) -> Optional[Livro]:
        """Remove um livro da biblioteca de um usuário pelo título. Retorna o livro removido."""
        if not self.existe_usuario(nome_usuario):
            return None
        
        biblioteca_atual_data = self.dados_usuarios['bibliotecas'].get(nome_usuario, [])
        livro_removido_data = None
        
        nova_biblioteca_data = []
        for livro_data in biblioteca_atual_data:
            if livro_data['titulo'] == titulo_livro:
                livro_removido_data = livro_data
            else:
                nova_biblioteca_data.append(livro_data)
        
        if livro_removido_data:
            self.dados_usuarios['bibliotecas'][nome_usuario] = nova_biblioteca_data
            self._salvar_dados_no_arquivo()
            return Livro.from_dict(livro_removido_data)
        return None

    def listar_todos_nomes_usuarios(self, incluir_admin=True) -> List[str]:
        """Retorna uma lista com os nomes de todos os usuários."""
        if incluir_admin:
            return list(self.dados_usuarios['usuarios'])
        else:
            return [u for u in self.dados_usuarios['usuarios'] if u != "admin"]