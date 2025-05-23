# from defs import *

# # DB
# livros.extend([
#     "Harry Potter",             "Senhor dos Anéis",        "O Hobbit",                        "Dom Quixote",                      "O Grande Gatsby",
#     "Moby Dick",                "Crime e Castigo",         "A Divina Comédia",                "Orgulho e Preconceito",            "Guerra e Paz",
#     "1984",                     "Ulisses",                 "O Morro dos Ventos Uivantes",     "Hamlet",                           "O Processo",
#     "O Retrato de Dorian Gray", "A Metamorfose",           "O Apanhador no Campo de Centeio", "As Aventuras de Huckleberry Finn", "Jane Eyre",
#     "Os Miseráveis",            "O Conde de Monte Cristo", "Anna Karenina",                   "A Letra Escarlate",                "O Sol é para Todos",
#     "A garota Do Lago",         "A Revolução dos Bichos",  "O Senhor das Moscas",             "Drácula",                          "Frankenstein",
#     "Admirável Mundo Novo",     "O Jardim Secreto",        "O Nome da Rosa",                  "Alice no País das Maravilhas",     "O Velho e o Mar",
#     "O Estrangeiro",            "O Pequeno Príncipe",      "O Homem Invisível",               "O Silmarillion",                   "As Crônicas de Nárnia",
#     "A Ilha do Tesouro",        "O Código Da Vinci",       "As Aventuras de Sherlock Holmes", "Os Irmãos Karamazov",              "O Diário de Anne Frank"
# ])

# generos.extend([
#     "Fantasia",   "Fantasia", "Aventura", "Aventura", "Clássico",
#     "Aventura",   "Drama",    "Poesia",   "Romance",  "Histórico",
#     "Distopia",   "Clássico", "Romance",  "Tragédia", "Ficção",
#     "Fantasia",   "Ficção",   "Ficção",   "Aventura", "Romance",
#     "Drama",      "Aventura", "Romance",  "Clássico", "Drama",
#     "Ficção",     "Distopia", "Distopia", "Terror",   "Terror",
#     "Distopia",   "Infantil", "Mistério", "Fantasia", "Clássico",
#     "Filosófico", "Infantil", "Ficção",   "Fantasia", "Fantasia",
#     "Aventura",   "Suspense", "Mistério", "Drama",    "Biografia"
# ])

# generos_map = {
#     "classico":   "Classico",   "clássico":   "Clássico",
#     "filosofico": "Filosofico", "filosófico": "Filosófico",
#     "portugues":  "Portugues",  "português":  "Português",
#     "tragedia":   "Tragedia",   "tragédia":   "Tragédia",
#     "misterio":   "Misterio",   "mistério":   "Mistério",
# #-----------------------------------------------------------#
#     "aventura":   "Aventura",   "biografia":  "Biografia",
#     "infantil":   "Infantil",   "distopia":   "Distopia",
#     "drama":      "Drama",      "fantasia":   "Fantasia",
#     "ficção":     "Ficção",     "poesia":     "Poesia",
#     "romance":    "Romance",    "suspense":   "Suspense",
#     "terror":     "Terror"
# }


import json
import os

# core/db.py

livros = [
    "Dom Casmurro",
    "O Senhor dos Anéis",
    "1984",
    "O Pequeno Príncipe"
]

generos = [
    "Ficção",
    "Fantasia",
    "Distopia",
    "Infantil"
]

usuarios = ["usuario1", "usuario2"]
senhas = ["senha1", "senha2"]

bibliotecas = {
    "usuario1": ["Dom Casmurro"],
    "usuario2": ["1984", "O Pequeno Príncipe"]
}


CAMINHO_LIVROS = "db/livros.json"

# Cria diretório db caso não exista
if not os.path.exists("db"):
    os.makedirs("db")

# Inicializa arquivo com alguns livros, se necessário
livros_iniciais = [
    {"titulo": "1984", "genero": "Distopia"},
    {"titulo": "Dom Quixote", "genero": "Romance"},
    {"titulo": "O Hobbit", "genero": "Fantasia"},
]

if not os.path.exists(CAMINHO_LIVROS):
    with open(CAMINHO_LIVROS, "w") as f:
        json.dump(livros_iniciais, f, indent=4, ensure_ascii=False)

def carregar_livros():
    with open(CAMINHO_LIVROS, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados

def salvar_livros(dados):
    with open(CAMINHO_LIVROS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
