from services.biblioteca import Biblioteca
import tkinter as tk
from tkinter import ttk
from ui.app import start_ui
from util.ui_util import atualizar_estado_combobox
from ui.tabela import inserir_livro_tabela

def subbtn_salvar_livro(root, biblioteca, tabela_livros, livro, titulo, autor, categoria, ano, lido, avaliacao, tela_popup, is_edicao:bool):
        livro_dict = {
            'titulo': titulo,
            'autor': autor,
            'categoria': categoria,
            'ano': int(ano),
            'lido': bool(lido),
            'avaliacao': int(avaliacao) if avaliacao else None,
        }

        if is_edicao:
            biblioteca.editar_livro(livro.id, livro_dict)
            start_ui(root)
        else:
            biblioteca.adicionar_livro(livro_dict)
            inserir_livro_tabela(tabela_livros, livro_dict)

        tela_popup.destroy()

def popup_crud_livro(root, biblioteca, tabela_livros, colunas_labels_para_telas_crud, livro_obj=None):
    '''Para adição (Create) e edição (Update) de livros pela GUI.
    Considerado adição se nenhum livro pre-existente for passado em livro_obj
    '''
    tela_popup = tk.Toplevel(root)
    tela_popup.title(f'{ "Editar" if livro_obj else "Adicionar" } Livro')
    tela_popup.geometry("300x380")

    entries = {}

    #campos de edição principais
    for label, atrib in colunas_labels_para_telas_crud.items():
        tk.Label(tela_popup, text=f"{label}:").pack()
        entry = tk.Entry(tela_popup)
        if livro_obj:
            entry.insert(0, getattr(livro_obj, atrib, ""))
        entries[atrib] = entry
        entry.pack()

    #para avaliação, cria um combobox com opções de 1 a 5, e apenas disponivel se lido for verdadeiro
    #mas nao da pack ainda
    avaliacao_var = tk.StringVar(value=getattr(livro_obj, 'avaliacao', ""))
    avaliacao_combobox = ttk.Combobox(tela_popup, textvariable=avaliacao_var, values=[i for i in range(1, 6)], state="readonly")
    #evento de atualizacao de estado é trigado ao mudar combobox
    avaliacao_combobox.bind("<<ComboboxSelected>>", lambda event: atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_salvaradd))

    #checkbox de lido
    lido_var = tk.BooleanVar(value=getattr(livro_obj, 'lido', False))
    tk.Label(tela_popup, text="Lido:").pack()
    tk.Checkbutton(tela_popup, text="Lido", variable=lido_var, command=lambda: atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_salvaradd)).pack()

    #label da combobox de avaliação
    tk.Label(tela_popup, text="Avaliação:").pack()

    #ao habilitar/desabilitar o checkbutton, atualiza estado da combobox
    avaliacao_combobox.pack()

    #Botão de salvar/adicionar.
    #Desabilitado se os campos obrigatorios forem vazios ou se lido for verdadeiro enquanto avaliação for vazia
    btn_salvaradd = tk.Button(
        tela_popup,
        text="Salvar" if livro_obj else "Adicionar",
        command=lambda: subbtn_salvar_livro(
                root,
                biblioteca,
                tabela_livros,
                livro_obj,
                entries['titulo'].get(),
                entries['autor'].get(),
                entries['categoria'].get(),
                entries['ano'].get(),
                lido_var.get(),
                avaliacao_var.get(),
                tela_popup,
                is_edicao=bool(livro_obj) # True se for edição, False se for adição de novo livro
            )
        )
    btn_salvaradd.pack(pady=10)

    atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_salvaradd) #atualizacao inicial