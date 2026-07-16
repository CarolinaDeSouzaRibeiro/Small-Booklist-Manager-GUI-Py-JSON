from services.biblioteca import Biblioteca
import tkinter as tk
from tkinter import ttk
from ui.app import start_ui

def adicionar_livro(biblioteca, root, colunas_labels_para_telas_crud):
    #pega a coluna selecionada na tabela

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

    #função para atualizar o estado do combobox de avaliação
    def atualizar_estado_combobox():
        avaliacao_combobox.config(state="normal" if lido_var.get() else "disabled")
        #se estiver vazio enquanto lido for verdadeiro, desabilita o botão de salvar
        if lido_var.get() and not avaliacao_var.get():
            btn_add.config(state="disabled")
        else:
            btn_add.config(state="normal")

    #para avaliação, cria um combobox com opções de 1 a 5, e apenas disponivel se lido for verdadeiro
    #mas nao da pack ainda
    avaliacao_var = tk.StringVar(value=None)
    avaliacao_combobox = ttk.Combobox(tela_edicao, textvariable=avaliacao_var, values=[i for i in range(1, 6)], state="readonly")
    #checkbox de lido
    lido_var = tk.BooleanVar(value=False)
    tk.Label(tela_edicao, text="Lido:").pack()
    tk.Checkbutton(tela_edicao, text="Lido", variable=lido_var, command=atualizar_estado_combobox).pack()

    #label da combobox de avaliação
    tk.Label(tela_edicao, text="Avaliação:").pack()

    #ao habilitar/desabilitar o checkbutton, atualiza estado da combobox
    avaliacao_combobox.pack()

    #Botão de salvar.
    #Desabilitado se os campos obrigatorios forem vazios ou se lido for verdadeiro enquanto avaliação for vazia
    def btn_adicionar_livro(titulo, autor, categoria, ano, lido, avaliacao, tela):
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

    btn_add = tk.Button(tela_edicao, text="Adicionar", command=lambda: btn_adicionar_livro(entries['titulo'].get(), entries['autor'].get(), entries['categoria'].get(), entries['ano'].get(), lido_var.get(), avaliacao_var.get(), tela_edicao))
    btn_add.pack(pady=10)

    atualizar_estado_combobox() #atualizacao inicial



def editar_livro(tabela_livros, biblioteca, root, colunas_labels_para_telas_crud):
    #pega a coluna selecionada na tabela
    livro_selecionado = tabela_livros.selection()
    if not livro_selecionado: return

    item = tabela_livros.item(livro_selecionado)
    livro_id = item['values'][-1]
    print(livro_id)

    livro_obj = biblioteca.livros[f'{livro_id}']

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

    #função para atualizar o estado do combobox de avaliação
    def atualizar_estado_combobox():
        avaliacao_combobox.config(state="normal" if lido_var.get() else "disabled")
        #se estiver vazio enquanto lido for verdadeiro, desabilita o botão de salvar
        if lido_var.get() and not avaliacao_var.get():
            btn_salvar.config(state="disabled")
        else:
            btn_salvar.config(state="normal")

    #para avaliação, cria um combobox com opções de 1 a 5, e apenas disponivel se lido for verdadeiro
    #mas nao da pack ainda
    avaliacao_var = tk.StringVar(value=livro_obj.avaliacao)
    avaliacao_combobox = ttk.Combobox(tela_edicao, textvariable=avaliacao_var, values=[i for i in range(1, 6)], state="readonly")
    #checkbox de lido
    lido_var = tk.BooleanVar(value=livro_obj.lido)
    tk.Label(tela_edicao, text="Lido:").pack()
    tk.Checkbutton(tela_edicao, text="Lido", variable=lido_var, command=atualizar_estado_combobox).pack()

    #label da combobox de avaliação
    tk.Label(tela_edicao, text="Avaliação:").pack()

    #ao habilitar/desabilitar o checkbutton, atualiza estado da combobox
    avaliacao_combobox.pack()

    #Botão de salvar.
    #Desabilitado se os campos obrigatorios forem vazios ou se lido for verdadeiro enquanto avaliação for vazia
    def salvar_edicao(livro, titulo, autor, categoria, ano, lido, avaliacao, tela):
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

        print(f'\nlivro id:{livro_id}\ndict atualizado:{livro_atualizado_dict}\n')

        biblioteca.editar_livro(livro.id, livro_atualizado_dict)

        tela.destroy()
        # root.destroy
        # app()
        start_ui(root)

    btn_salvar = tk.Button(tela_edicao, text="Salvar", command=lambda: salvar_edicao(livro_obj, entries['titulo'].get(), entries['autor'].get(), entries['categoria'].get(), entries['ano'].get(), lido_var.get(), avaliacao_var.get(), tela_edicao))
    btn_salvar.pack(pady=10)

    atualizar_estado_combobox() #atualizacao inicial




def btn_deletar_livro(tabela_livros, biblioteca, root):
    livro_selecionado = tabela_livros.selection()
    if not livro_selecionado: return

    item = tabela_livros.item(livro_selecionado)
    livro_id = item['values'][-1]
    print(livro_id)

    livro_obj = biblioteca.livros[f'{livro_id}']

    tela_confirmacao = tk.Toplevel(root)
    tela_confirmacao.title("Confirmar Exclusão")
    tela_confirmacao.geometry("300x200")
    tk.Label(tela_confirmacao, text=f"Tem certeza que deseja excluir o livro '{livro_obj.titulo}'?").pack(pady=20)
    
    def confirmar_exclusao():
        biblioteca.excluir_livro(int(livro_id))
        tabela_livros.delete(livro_selecionado)
        tela_confirmacao.destroy()
        # root.destroy
        # app()

    tk.Button(tela_confirmacao, text="Confirmar", command=confirmar_exclusao).pack(pady=10)
    tk.Button(tela_confirmacao, text="Cancelar", command=tela_confirmacao.destroy).pack(pady=10) #destroi tela se cancelar




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