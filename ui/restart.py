from services.biblioteca import Biblioteca
import tkinter as tk
from tkinter import ttk

def restart_ui(oldroot):
    import tkinter as tk
    from tkinter import ttk

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
    from ui.crud.editar import editar_livro
    from ui.crud.adicionar import adicionar_livro
    from ui.crud.delete import btn_deletar_livro

    import tkinter as tk
    from tkinter import ttk


    #botões
    btn_adicionar = tk.Button(newroot, text="Adicionar Livro", command=lambda: adicionar_livro(biblioteca, newroot, colunas_labels_para_telas_crud)    )
    btn_adicionar.pack(side="left", padx=5, pady=5)

    btn_editar = tk.Button(newroot, text="Editar Livro", command=lambda: editar_livro(tabela_livros, biblioteca, newroot, colunas_labels_para_telas_crud))
    btn_editar.pack(side="left", padx=5, pady=5)

    btn_excluir = tk.Button(newroot, text="Excluir Livro", command=lambda: btn_deletar_livro(tabela_livros, biblioteca, newroot))
    btn_excluir.pack(side="left", padx=5, pady=5)


    newroot.mainloop()

