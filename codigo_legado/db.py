from defs import *

# DB
livros.extend([
    "Harry Potter",             "Senhor dos Anéis",        "O Hobbit",                        "Dom Quixote",                      "O Grande Gatsby",
    "Moby Dick",                "Crime e Castigo",         "A Divina Comédia",                "Orgulho e Preconceito",            "Guerra e Paz",
    "1984",                     "Ulisses",                 "O Morro dos Ventos Uivantes",     "Hamlet",                           "O Processo",
    "O Retrato de Dorian Gray", "A Metamorfose",           "O Apanhador no Campo de Centeio", "As Aventuras de Huckleberry Finn", "Jane Eyre",
    "Os Miseráveis",            "O Conde de Monte Cristo", "Anna Karenina",                   "A Letra Escarlate",                "O Sol é para Todos",
    "A garota Do Lago",         "A Revolução dos Bichos",  "O Senhor das Moscas",             "Drácula",                          "Frankenstein",
    "Admirável Mundo Novo",     "O Jardim Secreto",        "O Nome da Rosa",                  "Alice no País das Maravilhas",     "O Velho e o Mar",
    "O Estrangeiro",            "O Pequeno Príncipe",      "O Homem Invisível",               "O Silmarillion",                   "As Crônicas de Nárnia",
    "A Ilha do Tesouro",        "O Código Da Vinci",       "As Aventuras de Sherlock Holmes", "Os Irmãos Karamazov",              "O Diário de Anne Frank"
])

generos.extend([
    "Fantasia",   "Fantasia", "Aventura", "Aventura", "Clássico",
    "Aventura",   "Drama",    "Poesia",   "Romance",  "Histórico",
    "Distopia",   "Clássico", "Romance",  "Tragédia", "Ficção",
    "Fantasia",   "Ficção",   "Ficção",   "Aventura", "Romance",
    "Drama",      "Aventura", "Romance",  "Clássico", "Drama",
    "Ficção",     "Distopia", "Distopia", "Terror",   "Terror",
    "Distopia",   "Infantil", "Mistério", "Fantasia", "Clássico",
    "Filosófico", "Infantil", "Ficção",   "Fantasia", "Fantasia",
    "Aventura",   "Suspense", "Mistério", "Drama",    "Biografia"
])

generos_map = {
    "classico":   "Classico",   "clássico":   "Clássico",
    "filosofico": "Filosofico", "filosófico": "Filosófico",
    "portugues":  "Portugues",  "português":  "Português",
    "tragedia":   "Tragedia",   "tragédia":   "Tragédia",
    "misterio":   "Misterio",   "mistério":   "Mistério",
#-----------------------------------------------------------#
    "aventura":   "Aventura",   "biografia":  "Biografia",
    "infantil":   "Infantil",   "distopia":   "Distopia",
    "drama":      "Drama",      "fantasia":   "Fantasia",
    "ficção":     "Ficção",     "poesia":     "Poesia",
    "romance":    "Romance",    "suspense":   "Suspense",
    "terror":     "Terror"
}