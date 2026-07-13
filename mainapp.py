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
from ui.crud.editar import editar_livro
from ui.crud.adicionar import adicionar_livro

import tkinter as tk
from tkinter import ttk


#botões
btn_adicionar = tk.Button(root, text="Adicionar Livro", command=lambda: adicionar_livro(tabela_livros, biblioteca, root, colunas_labels_para_telas_crud)    )
btn_adicionar.pack(side="left", padx=5, pady=5)

btn_editar = tk.Button(root, text="Editar Livro", command=lambda: editar_livro(tabela_livros, biblioteca, root, colunas_labels_para_telas_crud))
btn_editar.pack(side="left", padx=5, pady=5)

btn_excluir = tk.Button(root, text="Excluir Livro")
btn_excluir.pack(side="left", padx=5, pady=5)

btn_marcar_lido = tk.Button(root, text="Marcar como Lido/Não Lido")
btn_marcar_lido.pack(side="left", padx=5, pady=5)

root.mainloop()