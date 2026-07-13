from services.biblioteca import Biblioteca
import tkinter as tk
from tkinter import ttk

#TODO: separar interface e logica

biblioteca = Biblioteca()

root = tk.Tk()
root.geometry("600x400")

colunas_labels = {'Titulo':'titulo', 'Autor':'autor', 'Categoria':'categoria', 'Ano':'ano', 'Lido':'lido', 'Avaliação':'avaliacao', 'Data de Cadastro':'data_cadastro', 'ID interno':'id'}
tabela_livros = ttk.Treeview(root, columns=list(colunas_labels.values()), show='headings')

tabela_livros.pack(expand=True, fill='both')

#cria tabela
for label, col_id in colunas_labels.items():
    tabela_livros.heading(col_id, text=label)
    tabela_livros.column(col_id, width=100)

#popula tabela
for livro in biblioteca.livros.values():
    tabela_livros.insert("", "end", values=(livro.titulo, livro.autor, livro.categoria, livro.ano, livro.lido, livro.avaliacao, livro.data_cadastro, livro.id))

colunas_labels_para_telas_crud= {'Titulo':'titulo', 'Autor':'autor', 'Categoria':'categoria', 'Ano':'ano', 'Lido':'lido'}

#funções para os botões
def editar_livro():
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
        # if not titulo or not autor or not categoria or not ano:
        #     tk.messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos.")
        #     return
        # if lido and not avaliacao:
        #     tk.messagebox.showerror("Erro", "Se o livro foi lido, a avaliação deve ser preenchida.")
        #     return

        # print(f'val avaliacao:{avaliacao}')

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

        #atualiza tabela
        for item in tabela_livros.get_children():
            if tabela_livros.item(item)['values'][-1] == livro.id:
                tabela_livros.item(item, values=(livro.titulo, livro.autor, livro.categoria, livro.ano, livro.lido, livro.avaliacao, livro.data_cadastro, livro.id))
                break

        tela.destroy()
    btn_salvar = tk.Button(tela_edicao, text="Salvar", command=lambda: salvar_edicao(livro_obj, entries['titulo'].get(), entries['autor'].get(), entries['categoria'].get(), entries['ano'].get(), lido_var.get(), avaliacao_var.get(), tela_edicao))
    btn_salvar.pack(pady=10)

    atualizar_estado_combobox() #atualizacao inicial


#botões
btn_adicionar = tk.Button(root, text="Adicionar Livro")
btn_adicionar.pack(side="left", padx=5, pady=5)

btn_editar = tk.Button(root, text="Editar Livro", command=editar_livro)
btn_editar.pack(side="left", padx=5, pady=5)

btn_excluir = tk.Button(root, text="Excluir Livro")
btn_excluir.pack(side="left", padx=5, pady=5)

btn_marcar_lido = tk.Button(root, text="Marcar como Lido/Não Lido")
btn_marcar_lido.pack(side="left", padx=5, pady=5)

root.mainloop()