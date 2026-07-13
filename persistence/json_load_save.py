'''
Módulo responsável por gerenciar a persistência
dos livros no arquivo JSON.
'''
import json
from pathlib import Path
from models.livro import Livro
from datetime import date
# import datetime

# funções manipulação geral do json
def salvar_json_livros(livrosObjetos:dict, nome_json:str='livros.json'):
    '''Atualiza o JSON com os objetos livros
    no dict de execução da biblioteca.'''

    #se dicionario

    with open(nome_json, 'w') as f:
        json.dump(
            {livro.get_id(): livro.to_dict() for livro in livrosObjetos.values()
            }, f) if livrosObjetos else json.dump({}, f) # Se não houverem livros na lista, coloca um json vazio
        #TODO: forma mais otimizada de salvar json, sem reescrever sempre do zero

def carregar_livros_do_json(livrosObjetos={}, nome_json:str='livros.json'):
    '''Carrega os livros no JSON para o dicionario de livros de execução'''
    #caso livros.json não exista
    if not Path(nome_json).is_file():
        print(f'\n{nome_json} não encontrado.\nCriando novo arquivo...\n')
        return salvar_json_livros(livrosObjetos, nome_json)

    try:
        with open(nome_json, 'r') as f:
            livros_data = json.load(f)
            for livro_id_raw in livros_data:
                livro_dict = livros_data[livro_id_raw]
                livro_objeto = Livro.from_dict(livro_dict)
                livrosObjetos[livro_id_raw] = livro_objeto
            return livrosObjetos
    except:
        print(f'\nErro ao carregar {nome_json}.\nCriando backup...\n')
        Path(nome_json).rename(f'BACKUP_livros_{date.today().strftime("%Y-%m-%d_%H-%M-%S")}.json.bak')
        return salvar_json_livros(livrosObjetos, nome_json) #tenta restaurar, via o que houver no dict usado em execução. Caso não consiga, retornará um novo json vazio.