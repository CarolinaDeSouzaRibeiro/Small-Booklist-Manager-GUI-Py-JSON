def start_ui(oldroot=None):
    from services.biblioteca import Biblioteca
    import tkinter as tk
    from tkinter import ttk

    if oldroot:
        oldroot.destroy()

    biblioteca = Biblioteca()


    newroot = tk.Tk()
    newroot.title("Biblioteca")
    newroot.geometry("600x400")

    colunas_labels = {'Titulo':'titulo', 'Autor':'autor', 'Categoria':'categoria', 'Ano':'ano', 'Lido':'lido', 'Avaliação':'avaliacao', 'Data de Cadastro':'data_cadastro', 'ID interno':'id'}
    tabela_livros = ttk.Treeview(newroot, columns=list(colunas_labels.values()), show='headings')

    tabela_livros.pack(expand=True, fill='both')

    #cria tabela
    for label, col_id in colunas_labels.items():
        tabela_livros.heading(col_id, text=label)
        tabela_livros.column(col_id, width=100)


    #popula tabela
    for livro in biblioteca.livros.values():
        tabela_livros.insert("", "end", values=(livro.titulo, livro.autor, livro.categoria, livro.ano, livro.lido, livro.avaliacao, livro.data_cadastro, livro.id))

    colunas_labels_para_telas_crud= {'Titulo':'titulo', 'Autor':'autor', 'Categoria':'categoria', 'Ano':'ano'}

    #funções para os botões
    from ui.crud import onclick_btn_editar_livro, onclick_btn_add_livro, popup_deletar_livro, btn_buscar_livro

    #botões
    btn_adicionar = tk.Button(newroot, text="Adicionar Livro", command=lambda: onclick_btn_add_livro(newroot, biblioteca, tabela_livros, colunas_labels_para_telas_crud)    )
    btn_adicionar.pack(side="left", padx=5, pady=5)

    btn_editar = tk.Button(newroot, text="Editar Livro", command=lambda: onclick_btn_editar_livro(newroot, biblioteca, tabela_livros, colunas_labels_para_telas_crud))
    btn_editar.pack(side="left", padx=5, pady=5)

    btn_excluir = tk.Button(newroot, text="Excluir Livro", command=lambda: popup_deletar_livro(tabela_livros, biblioteca, newroot))
    btn_excluir.pack(side="left", padx=5, pady=5)

    #busca
    btn_buscar = tk.Button(newroot, text="Buscar Livro", command=lambda:btn_buscar_livro(newroot,biblioteca,tabela_livros))
    btn_buscar.pack(side="left", padx=5, pady=5)

    newroot.mainloop()

