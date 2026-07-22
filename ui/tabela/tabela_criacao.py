def criar_headers(colunas_labels, tabela_livros):
    '''Cria os headers das colunas da tabela'''
    for label, col_id in colunas_labels.items():
        tabela_livros.heading(col_id, text=label)
        tabela_livros.column(col_id, width=100)


def popular_tabela(livros:dict, tabela_livros):
    '''Preenche a tabela com os livros recebidos'''
    for livro in livros.values():
        tabela_livros.insert("", "end", values=(livro.titulo, livro.autor, livro.categoria, livro.ano, livro.lido, livro.avaliacao, livro.data_cadastro, livro.id))