from models.livro import Livro
from persistence.json_load_save import salvar_json_livros, carregar_livros_do_json

class Biblioteca:
    """Classe responsável pelas regras de negócio."""
    def __init__(self):
        self.livros = carregar_livros_do_json()

    #funções crud
    def adicionar_livro(self, novo_livro_dict:dict):
        novo_livro_obj = Livro.from_dict(novo_livro_dict)
        self.livros.append(novo_livro_obj)
        salvar_json_livros(self.livros) #atualiza json

    def editar_livro(self, id:int, livro_atualizado:dict):
        

    def excluir_livro(self, id:int): #TODO
        #Solicitar confirmação antes da exclusão.
        pass

    #funções de busca
    def buscar(self, termo:str): #TODO
        #obs:busca case-insensitive
        pass

