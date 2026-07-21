from services.biblioteca import Biblioteca
import tkinter as tk
from tkinter import ttk
from ui.app import start_ui
from util.ui_util import atualizar_estado_combobox

def subbtn_salvar_livro(root, biblioteca, livro, titulo, autor, categoria, ano, lido, avaliacao, tela_popup, is_edicao:bool):
        livro_atualizado_dict = {
            'titulo': titulo,
            'autor': autor,
            'categoria': categoria,
            'ano': int(ano),
            'lido': bool(lido),
            'avaliacao': int(avaliacao) if avaliacao else None,
        }

        # print(f'\nlivro id:{livro_id}\ndict atualizado:{livro_atualizado_dict}\n')

        if is_edicao:
            biblioteca.editar_livro(livro.id, livro_atualizado_dict)
        else:
            biblioteca.adicionar_livro(livro_atualizado_dict)

        tela_popup.destroy()
        start_ui(root)

def popup_crud_livro(biblioteca, root, colunas_labels_para_telas_crud, livro_obj=None):

    tela_edicao = tk.Toplevel(root)
    tela_edicao.title("Editar Livro" if livro_obj else "Adicionar Livro")
    tela_edicao.geometry("300x500")

    entries = {}

    #campos de edição principais
    for label, atrib in colunas_labels_para_telas_crud.items():
        tk.Label(tela_edicao, text=f"{label}:").pack()
        entry = tk.Entry(tela_edicao)
        if livro_obj:
            entry.insert(0, getattr(livro_obj, atrib))
        entries[atrib] = entry
        entry.pack()

    #para avaliação, cria um combobox com opções de 1 a 5, e apenas disponivel se lido for verdadeiro
    #mas nao da pack ainda
    avaliacao_var = tk.StringVar(value=getattr(livro_obj, 'avaliacao', ""))
    avaliacao_combobox = ttk.Combobox(tela_edicao, textvariable=avaliacao_var, values=[i for i in range(1, 6)], state="readonly")
    #evento de atualizacao de estado é trigado ao mudar combobox
    avaliacao_combobox.bind("<<ComboboxSelected>>", lambda event: atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_salvaradd))

    #checkbox de lido
    lido_var = tk.BooleanVar(value=getattr(livro_obj, 'lido', False))
    tk.Label(tela_edicao, text="Lido:").pack()
    tk.Checkbutton(tela_edicao, text="Lido", variable=lido_var, command=lambda: atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_salvaradd)).pack()

    #label da combobox de avaliação
    tk.Label(tela_edicao, text="Avaliação:").pack()

    #ao habilitar/desabilitar o checkbutton, atualiza estado da combobox
    avaliacao_combobox.pack()

    #Botão de salvar/adicionar.
    #Desabilitado se os campos obrigatorios forem vazios ou se lido for verdadeiro enquanto avaliação for vazia
    


    btn_salvaradd = tk.Button(
        tela_edicao,
        text="Salvar" if livro_obj else "Adicionar",
        command=lambda: subbtn_salvar_livro(
                root,
                biblioteca,
                livro_obj,
                entries['titulo'].get(),
                entries['autor'].get(),
                entries['categoria'].get(),
                entries['ano'].get(),
                lido_var.get(),
                avaliacao_var.get(),
                tela_edicao,
                is_edicao=bool(livro_obj) # True se for edição, False se for adição de novo livro
            )
        )
    btn_salvaradd.pack(pady=10)

    atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_salvaradd) #atualizacao inicial

