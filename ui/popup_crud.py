from models.livro import Livro
import tkinter as tk
from tkinter import ttk
from ui.tabela.tabela_manuseio import inserir_livro_tabela
from util.ui_util import atualizar_estado_combo_e_btn
from ui.tabela.tabela_manuseio import editar_livro_tabela

def subbtn_salvar_livro(novo_livro:dict, biblioteca, tabela_livros:ttk.Treeview, tela_popup:tk.Toplevel, livro_og:Livro=None):
        if livro_og:
            biblioteca.editar_livro(livro_og.id, novo_livro)
            editar_livro_tabela(tabela_livros, livro_og.id, novo_livro)
        else:
            biblioteca.adicionar_livro(novo_livro)
            inserir_livro_tabela(tabela_livros, novo_livro)

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

    #combobox avaliacao
    #(não pode dar pack antes do checkbox lido setado)
    avaliacao_var = tk.StringVar(value=getattr(livro_obj, 'avaliacao', ""))
    avaliacao_combobox = ttk.Combobox(tela_popup, textvariable=avaliacao_var, values=[i for i in range(1, 6)], state="readonly")

    #evento de atualizar estados, ao mudar seleção.
    avaliacao_combobox.bind("<<ComboboxSelected>>", lambda event: atualizar_estado_combo_e_btn(avaliacao_combobox, lido_var, avaliacao_var, btn_salvaradd))

    #checkbox de lido
    lido_var = tk.BooleanVar(value=getattr(livro_obj, 'lido', False))
    tk.Checkbutton(tela_popup, text="Lido", variable=lido_var, command=lambda: atualizar_estado_combo_e_btn(avaliacao_combobox, lido_var, avaliacao_var, btn_salvaradd)).pack()

    #combobox de avaliação
    tk.Label(tela_popup, text="Avaliação:").pack()
    avaliacao_combobox.pack()

    #Botão de salvar/adicionar.
    #Desabilitado se os campos obrigatorios forem vazios ou se lido for verdadeiro enquanto avaliação for vazia
    btn_salvaradd = tk.Button(
        tela_popup,
        text="Salvar" if livro_obj else "Adicionar",
        command=lambda: subbtn_salvar_livro(
                novo_livro = popup_inputs_to_dict(entries, lido_var, avaliacao_var),
                biblioteca = biblioteca,
                tabela_livros = tabela_livros,
                tela_popup = tela_popup,
                livro_og = livro_obj
            )
        )
    btn_salvaradd.pack(pady=10)

    atualizar_estado_combo_e_btn(avaliacao_combobox, lido_var, avaliacao_var, btn_salvaradd) #atualizacao inicial



def popup_inputs_to_dict(entries_dict, lido_var, avaliacao_var):
    '''Converte o dicionário de entradas principais e as variáveis de estado em um dicionário de valores formatado para a biblioteca'''
    return {
        'titulo': entries_dict['titulo'].get(),
        'autor': entries_dict['autor'].get(),
        'categoria': entries_dict['categoria'].get(),
        'ano': int(entries_dict['ano'].get()),
        'lido': bool(lido_var.get()),
        'avaliacao': int(avaliacao_var.get()) if avaliacao_var.get() else None,
    }