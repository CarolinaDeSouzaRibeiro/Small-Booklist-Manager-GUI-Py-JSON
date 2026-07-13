import tkinter as tk
from tkinter import ttk
# from ui.app import app

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
        # root.destroy
        # app()

    btn_add = tk.Button(tela_edicao, text="Adicionar", command=lambda: btn_adicionar_livro(entries['titulo'].get(), entries['autor'].get(), entries['categoria'].get(), entries['ano'].get(), lido_var.get(), avaliacao_var.get(), tela_edicao))
    btn_add.pack(pady=10)

    atualizar_estado_combobox() #atualizacao inicial
