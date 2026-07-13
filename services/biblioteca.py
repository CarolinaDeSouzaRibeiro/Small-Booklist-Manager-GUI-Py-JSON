from models.livro import Livro
from persistence.json_load_save import salvar_json_livros, carregar_livros_do_json

class Biblioteca:
    """Classe responsável pelas regras de negócio."""
    def __init__(self):
        self.livros = carregar_livros_do_json()

    #funções crud
    def adicionar_livro(self, novo_livro_dict:dict):
        novo_livro_obj = Livro.from_dict(novo_livro_dict)
        self.livros[novo_livro_obj.id] = novo_livro_obj
        salvar_json_livros(self.livros) #atualiza json

    def editar_livro(self, id:int, livro_atualizado:dict):
        self.livros[id] = Livro.from_dict(livro_atualizado)
        salvar_json_livros(self.livros) #atualiza json

    def excluir_livro(self, id:int):
        del self.livros[f'{id}']
        salvar_json_livros(self.livros) #atualiza json


    #funções de busca
    def buscar(self, termo:str, buscar_por:str):
        #obs:busca case-insensitive
        resultados = []

        if buscar_por not in ['titulo', 'autor', 'categoria']:
            raise ValueError('\nCampo de busca inválido.\nUse \'titulo\', \'autor\' ou \'categoria\'.')

        for livro in self.livros.values():
            if termo.lower() in livro.to_dict()[buscar_por].lower():
                resultados.append(livro)
        return resultados