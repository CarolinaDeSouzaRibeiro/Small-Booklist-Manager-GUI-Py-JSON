from services.biblioteca import Biblioteca
import tkinter as tk
from tkinter import ttk
from ui.app import start_ui
from util.ui_util import get_livro_from_table_selection, atualizar_estado_combobox

def popup_adicionar_livro(biblioteca, root, colunas_labels_para_telas_crud):
    tela_edicao = tk.Toplevel(root)
    tela_edicao.title("Editar Livro")
    tela_edicao.geometry("300x500")

    entries = {}

    #campos de edição principais
    for label, atrib in colunas_labels_para_telas_crud.items():
        tk.Label(tela_edicao, text=f"{label}:").pack()
        entry = tk.Entry(tela_edicao)
        entries[atrib] = entry
        entry.pack()

    #para avaliação, cria um combobox com opções de 1 a 5, e apenas disponivel se lido for verdadeiro
    #mas nao da pack ainda
    avaliacao_var = tk.StringVar(value=None)
    avaliacao_combobox = ttk.Combobox(tela_edicao, textvariable=avaliacao_var, values=[i for i in range(1, 6)], state="readonly")
    #evento de atualizacao de estado é trigado ao mudar combobox
    avaliacao_combobox.bind("<<ComboboxSelected>>", lambda event: atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_add))

    #checkbox de lido
    lido_var = tk.BooleanVar(value=False)
    tk.Label(tela_edicao, text="Lido:").pack()
    tk.Checkbutton(tela_edicao, text="Lido", variable=lido_var, command=lambda: atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_add)).pack()

    #label da combobox de avaliação
    tk.Label(tela_edicao, text="Avaliação:").pack()

    #ao habilitar/desabilitar o checkbutton, atualiza estado da combobox
    avaliacao_combobox.pack()

    #Botão de salvar.
    #Desabilitado se os campos obrigatorios forem vazios ou se lido for verdadeiro enquanto avaliação for vazia
    def subbtn_adicionar_livro(titulo, autor, categoria, ano, lido, avaliacao, tela):
        '''Refere-se ao botão "adicionar livro" dentro do Popup de adicionar livro
        Não ao botão "adicionar livro" da tela principal!'''
        # if not titulo or not autor or not categoria or not ano:
        #     tk.messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos.")
        #     return
        # if lido and not avaliacao:
        #     tk.messagebox.showerror("Erro", "Se o livro foi lido, a avaliação deve ser preenchida.")
        #     return

        novo_livro_dict = {
            'titulo': titulo,
            'autor': autor,
            'categoria': categoria,
            'ano': int(ano),
            'lido': bool(lido),
            'avaliacao': int(avaliacao) if avaliacao else None,
        }


        biblioteca.adicionar_livro(novo_livro_dict)
        tela.destroy()
        start_ui(root)

    btn_add = tk.Button(tela_edicao, text="Adicionar", command=lambda: subbtn_adicionar_livro(entries['titulo'].get(), entries['autor'].get(), entries['categoria'].get(), entries['ano'].get(), lido_var.get(), avaliacao_var.get(), tela_edicao))
    btn_add.pack(pady=10)

    atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_add) #atualizacao inicial


def popup_editar_livro(tabela_livros, biblioteca, root, colunas_labels_para_telas_crud):
    livro_id, livro_selecionado = get_livro_from_table_selection(tabela_livros)
    if not livro_id: return #sem seleção, apenas ignorar clique do botão

    livro_obj = biblioteca.livros.get(f'{livro_id}')

    tela_edicao = tk.Toplevel(root)
    tela_edicao.title("Editar Livro")
    tela_edicao.geometry("300x500")

    entries = {}

    #campos de edição principais
    for label, atrib in colunas_labels_para_telas_crud.items():
        tk.Label(tela_edicao, text=f"{label}:").pack()
        entry = tk.Entry(tela_edicao)
        entry.insert(0, getattr(livro_obj, atrib))
        entries[atrib] = entry
        entry.pack()

    #para avaliação, cria um combobox com opções de 1 a 5, e apenas disponivel se lido for verdadeiro
    #mas nao da pack ainda
    avaliacao_var = tk.StringVar(value=livro_obj.avaliacao)
    avaliacao_combobox = ttk.Combobox(tela_edicao, textvariable=avaliacao_var, values=[i for i in range(1, 6)], state="readonly")
    #evento de atualizacao de estado é trigado ao mudar combobox
    avaliacao_combobox.bind("<<ComboboxSelected>>", lambda event: atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_salvar))

    #checkbox de lido
    lido_var = tk.BooleanVar(value=livro_obj.lido)
    tk.Label(tela_edicao, text="Lido:").pack()
    tk.Checkbutton(tela_edicao, text="Lido", variable=lido_var, command=lambda: atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_salvar)).pack()

    #label da combobox de avaliação
    tk.Label(tela_edicao, text="Avaliação:").pack()

    #ao habilitar/desabilitar o checkbutton, atualiza estado da combobox
    avaliacao_combobox.pack()

    #Botão de salvar.
    #Desabilitado se os campos obrigatorios forem vazios ou se lido for verdadeiro enquanto avaliação for vazia
    def subbtn_salvar_edicao(livro, titulo, autor, categoria, ano, lido, avaliacao, tela):
        '''Utilizado pelo botão "salvar" dentro do popup de edição de livro.
        Não confundir com o botão "editar livro" da tela principal.'''
        if not titulo or not autor or not categoria or not ano:
            tk.messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos.")
            return
        if lido and not avaliacao:
            tk.messagebox.showerror("Erro", "Se o livro foi lido, a avaliação deve ser preenchida.")
            return

        livro_atualizado_dict = {
            'titulo': titulo,
            'autor': autor,
            'categoria': categoria,
            'ano': int(ano),
            'lido': bool(lido),
            'avaliacao': int(avaliacao) if avaliacao else None,
        }

        # print(f'\nlivro id:{livro_id}\ndict atualizado:{livro_atualizado_dict}\n')

        biblioteca.editar_livro(livro.id, livro_atualizado_dict)

        tela.destroy()
        start_ui(root)

    btn_salvar = tk.Button(tela_edicao, text="Salvar", command=lambda: subbtn_salvar_edicao(livro_obj, entries['titulo'].get(), entries['autor'].get(), entries['categoria'].get(), entries['ano'].get(), lido_var.get(), avaliacao_var.get(), tela_edicao))
    btn_salvar.pack(pady=10)

    atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_salvar) #atualizacao inicial



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
    btn_adicionar = tk.Button(busca_root, text="Adicionar Livro", command=lambda: popup_adicionar_livro(biblioteca, busca_root, colunas_labels_para_telas_crud)    )
    btn_adicionar.pack(side="left", padx=5, pady=5)

    btn_editar = tk.Button(busca_root, text="Editar Livro", command=lambda: popup_editar_livro(tabela_livros, biblioteca, busca_root, colunas_labels_para_telas_crud))
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