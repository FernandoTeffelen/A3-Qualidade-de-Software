import json
import os
from typing import Dict, List, Optional, Tuple
from models.livro import Livro # Para type hinting da biblioteca do usuário

class RepositorioUsuarios:
    def __init__(self, caminho_arquivo_usuarios: str = "db/usuarios.json"):
        # Inicializa_o_repositorio_de_usuarios_com_o_caminho_do_arquivo_especificado
        self.caminho_arquivo = caminho_arquivo_usuarios
        self._garantir_arquivo_existente()
        self.dados_usuarios: Dict = self._carregar_dados_do_arquivo()

    def _garantir_arquivo_existente(self):
        # Garante_que_o_diretorio_e_o_arquivo_de_usuarios_existam_criando_os_se_necessario
        os.makedirs(os.path.dirname(self.caminho_arquivo), exist_ok=True)
        if not os.path.exists(self.caminho_arquivo):
            dados_iniciais = {
                "usuarios": ["admin"],
                "senhas": {"admin": "admin"},
                "bibliotecas": {"admin": []}
            }
            self._salvar_dados_no_arquivo(dados_iniciais)

    def _carregar_dados_do_arquivo(self) -> Dict:
        # Carrega_os_dados_dos_usuarios_do_arquivo_JSON_e_normaliza_a_estrutura
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read().strip()
                if not conteudo:
                    dados_iniciais = {"usuarios": ["admin"], "senhas": {"admin": "admin"}, "bibliotecas": {"admin": []}}
                    self._salvar_dados_no_arquivo(dados_iniciais)
                    return dados_iniciais
                
                dados = json.loads(conteudo)
                if "usuarios" not in dados: dados["usuarios"] = []
                if "senhas" not in dados: dados["senhas"] = {}
                if "bibliotecas" not in dados: dados["bibliotecas"] = {}

                if "admin" not in dados["usuarios"]:
                    dados["usuarios"].append("admin")
                    dados["senhas"]["admin"] = "admin"
                    dados["bibliotecas"]["admin"] = dados["bibliotecas"].get("admin", [])
                
                for nome_usuario, livros_serializados in dados["bibliotecas"].items():
                    biblioteca_corrigida = []
                    for item_livro in livros_serializados:
                        if isinstance(item_livro, str):
                            biblioteca_corrigida.append({"titulo": item_livro, "genero": "Desconhecido"})
                        elif isinstance(item_livro, dict) and "titulo" in item_livro and "genero" in item_livro:
                            biblioteca_corrigida.append(item_livro)
                    dados["bibliotecas"][nome_usuario] = biblioteca_corrigida
                return dados
        except (FileNotFoundError, json.JSONDecodeError):
            dados_iniciais = {"usuarios": ["admin"], "senhas": {"admin": "admin"}, "bibliotecas": {"admin": []}}
            self._salvar_dados_no_arquivo(dados_iniciais)
            return dados_iniciais

    def _salvar_dados_no_arquivo(self, dados: Optional[Dict] = None):
        # Salva_os_dados_dos_usuarios_no_arquivo_JSON
        dados_para_salvar = dados if dados is not None else self.dados_usuarios
        with open(self.caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)

    def buscar_senha(self, nome_usuario: str) -> Optional[str]:
        # Retorna_a_senha_de_um_usuario_especifico_se_ele_existir
        return self.dados_usuarios.get("senhas", {}).get(nome_usuario)

    def existe_usuario(self, nome_usuario: str) -> bool:
        # Verifica_se_um_usuario_com_o_nome_fornecido_existe_no_repositorio
        return nome_usuario in self.dados_usuarios.get("usuarios", [])

    def adicionar_usuario(self, nome_usuario: str, senha: str) -> bool:
        # Adiciona_um_novo_usuario_ao_repositorio_retornando_True_em_sucesso
        if self.existe_usuario(nome_usuario):
            return False
        
        self.dados_usuarios.setdefault("usuarios", []).append(nome_usuario)
        self.dados_usuarios.setdefault("senhas", {})[nome_usuario] = senha
        self.dados_usuarios.setdefault("bibliotecas", {})[nome_usuario] = []
        self._salvar_dados_no_arquivo()
        return True

    def remover_usuario(self, nome_usuario: str) -> bool:
        # Remove_um_usuario_do_repositorio_retornando_True_em_sucesso
        if nome_usuario == "admin":
            return False
        if not self.existe_usuario(nome_usuario):
            return False
        
        if nome_usuario in self.dados_usuarios.get("usuarios", []):
            self.dados_usuarios["usuarios"].remove(nome_usuario)
        self.dados_usuarios.get("senhas", {}).pop(nome_usuario, None)
        self.dados_usuarios.get("bibliotecas", {}).pop(nome_usuario, None)
        self._salvar_dados_no_arquivo()
        return True

    def alterar_dados_usuario(self, nome_antigo: str, novo_nome: Optional[str], nova_senha: Optional[str]) -> Tuple[bool, str]:
        # Altera_o_nome_de_usuario_e_ou_senha_de_um_usuario_existente
        if not self.existe_usuario(nome_antigo):
            return False, "Usuário a ser alterado não encontrado."

        nome_para_atualizar_senha = nome_antigo

        if novo_nome and novo_nome != nome_antigo:
            if self.existe_usuario(novo_nome):
                return False, f"Novo nome de usuário '{novo_nome}' já está em uso."
            idx = self.dados_usuarios['usuarios'].index(nome_antigo)
            self.dados_usuarios['usuarios'][idx] = novo_nome
            
            self.dados_usuarios['senhas'][novo_nome] = self.dados_usuarios['senhas'].pop(nome_antigo)
            self.dados_usuarios['bibliotecas'][novo_nome] = self.dados_usuarios['bibliotecas'].pop(nome_antigo, [])
            nome_para_atualizar_senha = novo_nome # Se o nome mudou, a senha deve ser atribuída ao novo nome
        
        if nova_senha:
            self.dados_usuarios["senhas"][nome_para_atualizar_senha] = nova_senha
        
        self._salvar_dados_no_arquivo()
        return True, "Dados do usuário alterados com sucesso."

    def obter_biblioteca_usuario(self, nome_usuario: str) -> List[Livro]:
        # Retorna_a_lista_de_objetos_Livro_da_biblioteca_de_um_usuario
        livros_data = self.dados_usuarios.get("bibliotecas", {}).get(nome_usuario, [])
        return [Livro.from_dict(data) for data in livros_data if isinstance(data, dict)]

    def adicionar_livro_na_biblioteca_usuario(self, nome_usuario: str, livro: Livro) -> bool:
        # Adiciona_um_livro_objeto_Livro_a_biblioteca_de_um_usuario
        if not self.existe_usuario(nome_usuario):
            return False
        
        biblioteca_atual_data = self.dados_usuarios['bibliotecas'].get(nome_usuario, [])
        # Evita duplicatas pelo título do livro
        if not any(l['titulo'] == livro.titulo for l in biblioteca_atual_data if isinstance(l, dict)):
            biblioteca_atual_data.append(livro.to_dict())
            self.dados_usuarios['bibliotecas'][nome_usuario] = biblioteca_atual_data
            self._salvar_dados_no_arquivo()
            return True
        return False

    def remover_livro_da_biblioteca_usuario(self, nome_usuario: str, titulo_livro: str) -> Optional[Livro]:
        # Remove_um_livro_da_biblioteca_de_um_usuario_pelo_titulo
        if not self.existe_usuario(nome_usuario):
            return None
        
        biblioteca_usuario_data = self.dados_usuarios.get("bibliotecas", {}).get(nome_usuario, [])
        livro_removido_obj = None
        
        nova_biblioteca_data = []
        for livro_data in biblioteca_usuario_data:
            if isinstance(livro_data, dict) and livro_data.get("titulo") == titulo_livro:
                livro_removido_obj = Livro.from_dict(livro_data)
            else:
                nova_biblioteca_data.append(livro_data)
        
        if livro_removido_obj:
            self.dados_usuarios["bibliotecas"][nome_usuario] = nova_biblioteca_data
            self._salvar_dados_no_arquivo()
            return livro_removido_obj
        return None

    def listar_todos_nomes_usuarios(self, incluir_admin=True) -> List[str]:
        # Retorna_uma_lista_com_os_nomes_de_todos_os_usuarios_cadastrados
        todos_usuarios = list(self.dados_usuarios.get("usuarios", []))
        if incluir_admin:
            return todos_usuarios
        else:
            return [u for u in todos_usuarios if u != "admin"]