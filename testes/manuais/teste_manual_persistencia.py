from models.livro import Livro
from persistence.json_load_save import salvar_json_livros, carregar_livros_do_json


dict_teste1 = {
        "titulo": "O Senhor dos Anéis",
        "autor": "J.R.R. Tolkien",
        "ano": 1954,
        "categoria": "Fantasia",
        "lido": False,
        "avaliacao": None,
        "data_cadastro": None
    }
dict_teste2 = {
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "ano": 1899,
        "categoria": "Romance",
        "lido": True,
        "avaliacao": 5,
        "data_cadastro": "2026-07-11"
    }

salvar_json_livros([Livro(**dict_teste1), Livro(**dict_teste2)], 'livros.json')

livros = carregar_livros_do_json({})