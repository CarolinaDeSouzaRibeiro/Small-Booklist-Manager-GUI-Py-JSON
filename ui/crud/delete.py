import tkinter as tk
from tkinter import ttk
# from ui.app import app


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

