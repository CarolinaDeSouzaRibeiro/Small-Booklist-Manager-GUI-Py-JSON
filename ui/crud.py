from services.biblioteca import Biblioteca
import tkinter as tk
from tkinter import ttk
from ui.app import start_tela_principal
from util.ui_util import get_livro_from_table_selection, atualizar_estado_combo_e_btn
from ui.popup_crud import popup_crud_livro

def onclick_btn_add_livro(root, biblioteca, tabela_livros, colunas_labels_para_telas_crud):
    popup_crud_livro(
        root,
        biblioteca,
        tabela_livros,
        colunas_labels_para_telas_crud
    )


def onclick_btn_editar_livro(root, biblioteca, tabela_livros, colunas_labels_para_telas_crud):
    livro_id, livro_selecionado = get_livro_from_table_selection(tabela_livros)
    if not livro_id: return #sem seleção, apenas ignorar clique do botão

    livro_obj = biblioteca.livros.get(f'{livro_id}')

    popup_crud_livro(
        root,
        biblioteca,
        tabela_livros,
        colunas_labels_para_telas_crud,
        livro_preexistente_obj=livro_obj
    )


def popup_deletar_livro(tabela_livros, biblioteca, root):
    livro_id, livro_selecionado = get_livro_from_table_selection(tabela_livros)
    if not livro_id: return #sem seleção, apenas ignorar clique do botão

    livro_obj = biblioteca.livros.get(f'{livro_id}')

    tela_confirmacao = tk.Toplevel(root)
    tela_confirmacao.title("Confirmar Exclusão")
    tela_confirmacao.geometry("300x200")
    tk.Label(tela_confirmacao, text=f"Tem certeza que deseja excluir o livro '{livro_obj.titulo}'?").pack(pady=20)

    def subbtn_confirmar_exclusao():
        biblioteca.excluir_livro(int(livro_id))
        tabela_livros.delete(livro_selecionado)
        tela_confirmacao.destroy()

    tk.Button(tela_confirmacao, text="Confirmar", command=subbtn_confirmar_exclusao).pack(pady=10)
    tk.Button(tela_confirmacao, text="Cancelar", command=tela_confirmacao.destroy).pack(pady=10) #destroi tela se cancelar




def popup_resultados_busca(biblioteca, resultados_busca):
    import tkinter as tk
    from tkinter import ttk
    #busca
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



    #popula tabela com resultados da busca
    for livro in resultados_busca:
        tabela_livros.insert("", "end", values=(livro.titulo, livro.autor, livro.categoria, livro.ano, livro.lido, livro.avaliacao, livro.data_cadastro, livro.id))

    colunas_labels_para_telas_crud= {'Titulo':'titulo', 'Autor':'autor', 'Categoria':'categoria', 'Ano':'ano'}

    import tkinter as tk
    from tkinter import ttk


    #botões
    btn_adicionar = tk.Button(busca_root, text="Adicionar Livro", command=lambda: onclick_btn_add_livro(biblioteca, busca_root, colunas_labels_para_telas_crud)    )
    btn_adicionar.pack(side="left", padx=5, pady=5)

    btn_editar = tk.Button(busca_root, text="Editar Livro", command=lambda: onclick_btn_editar_livro(tabela_livros, biblioteca, busca_root, colunas_labels_para_telas_crud))
    btn_editar.pack(side="left", padx=5, pady=5)

    btn_excluir = tk.Button(busca_root, text="Excluir Livro", command=lambda: popup_deletar_livro(tabela_livros, biblioteca, busca_root))
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

    def onclick_subbtn_realizar_busca():
        termo = entry_busca.get()
        campo_a_buscar = campo_var.get()
        tela_busca.destroy()
        resultados_busca = biblioteca.buscar(termo, campo_a_buscar)
        popup_resultados_busca(biblioteca, resultados_busca)

    btn_realizar_busca = tk.Button(tela_busca, text="Realizar Busca", command=onclick_subbtn_realizar_busca)
    btn_realizar_busca.pack(pady=10)