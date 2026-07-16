def criar_labels_tabela(colunas_labels, tabela_livros):
    for label, col_id in colunas_labels.items():
        tabela_livros.heading(col_id, text=label)
        tabela_livros.column(col_id, width=100)


def inserir_livro_tabela(tabela_livros, livro):
    tabela_livros.insert("", "end", values=(
        livro.titulo,
        livro.autor,
        livro.categoria,
        livro.ano,
        livro.lido,
        livro.avaliacao,
        livro.data_cadastro,
        livro.id
    ))