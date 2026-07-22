from models.livro import Livro

def criar_labels_tabela(colunas_labels, tabela_livros):
    for label, col_id in colunas_labels.items():
        tabela_livros.heading(col_id, text=label)
        tabela_livros.column(col_id, width=100)


def inserir_livro_tabela(tabela_livros, novo_livro):
    '''Insere um livro na tabela de livros da GUI.
    Aceita tanto um objeto Livro quanto um dicionário.
    '''
    if isinstance(novo_livro, dict):
        #converte dict pra objeto livro
        novo_livro = Livro.from_dict(novo_livro)
    tabela_livros.insert("", "end", values=(
        novo_livro.titulo,
        novo_livro.autor,
        novo_livro.categoria,
        novo_livro.ano,
        novo_livro.lido,
        novo_livro.avaliacao,
        novo_livro.data_cadastro,
        novo_livro.id
    ))