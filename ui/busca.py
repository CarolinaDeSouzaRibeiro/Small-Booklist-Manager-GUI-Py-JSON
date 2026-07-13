from services.biblioteca import Biblioteca
import tkinter as tk
from tkinter import ttk

def app_busca(biblioteca,busca_termo, busca_campo):
    import tkinter as tk
    from tkinter import ttk
    busca_root = tk.Tk()
    busca_root.title("Resultados da Busca")
    busca_root.geometry("600x400")

    colunas_labels = {'Titulo':'titulo', 'Autor':'autor', 'Categoria':'categoria', 'Ano':'ano', 'Lido':'lido', 'Avaliação':'avaliacao', 'Data de Cadastro':'data_cadastro', 'ID interno':'id'}
    tabela_livros = ttk.Treeview(busca_root, columns=list(colunas_labels.values()), show='headings')

    tabela_livros.pack(expand=True, fill='both')

    #cria tabela
    for label, col_id in colunas_labels.items():
        tabela_livros.heading(col_id, text=label)
        tabela_livros.column(col_id, width=100)


    #pega os resultados da busca
    resultados_busca = biblioteca.buscar(busca_termo, busca_campo)

    #popula tabela com resultados da busca
    for livro in resultados_busca:
        tabela_livros.insert("", "end", values=(livro.titulo, livro.autor, livro.categoria, livro.ano, livro.lido, livro.avaliacao, livro.data_cadastro, livro.id))

    colunas_labels_para_telas_crud= {'Titulo':'titulo', 'Autor':'autor', 'Categoria':'categoria', 'Ano':'ano'}

    #funções para os botões
    from ui.crud.editar import editar_livro
    from ui.crud.adicionar import adicionar_livro
    from ui.crud.delete import btn_deletar_livro

    import tkinter as tk
    from tkinter import ttk


    #botões
    btn_adicionar = tk.Button(busca_root, text="Adicionar Livro", command=lambda: adicionar_livro(biblioteca, busca_root, colunas_labels_para_telas_crud)    )
    btn_adicionar.pack(side="left", padx=5, pady=5)

    btn_editar = tk.Button(busca_root, text="Editar Livro", command=lambda: editar_livro(tabela_livros, biblioteca, busca_root, colunas_labels_para_telas_crud))
    btn_editar.pack(side="left", padx=5, pady=5)

    btn_excluir = tk.Button(busca_root, text="Excluir Livro", command=lambda: btn_deletar_livro(tabela_livros, biblioteca, busca_root))
    btn_excluir.pack(side="left", padx=5, pady=5)


    busca_root.mainloop()


def btn_buscar_livro(root, biblioteca, tabela_livros):
    tela_busca = tk.Toplevel(root)
    tela_busca.title("Buscar Livro")
    tela_busca.geometry("400x300")

    label_busca = tk.Label(tela_busca, text="Termo a buscar:").pack()
    entry_busca = tk.Entry(tela_busca)
    entry_busca.pack(pady=10)

    #opção pra escolher o campo a ser buscado
    label_campo = tk.Label(tela_busca, text="Campo a buscar:").pack()
    campo_var = tk.StringVar(value="titulo")
    campo_dropdown = tk.OptionMenu(tela_busca, campo_var, "titulo", "autor", "categoria", "ano")
    campo_dropdown.pack(pady=10)

    def realizar_busca():
        termo = entry_busca.get()
        campo_a_buscar = campo_var.get()
        tela_busca.destroy()
        app_busca(biblioteca, termo, campo_a_buscar)

    btn_realizar_busca = tk.Button(tela_busca, text="Realizar Busca", command=realizar_busca)
    btn_realizar_busca.pack(pady=10)