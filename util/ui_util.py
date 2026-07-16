def get_livro_from_table_selection(tabela_livros):
    '''Recebe uma tabela tkinter tree com livros
    Se um elemento estiver selecionado, retorna o ID e a seleção do livro'''
    #pega a coluna selecionada na tabela
    livro_selecionado = tabela_livros.selection()
    if not livro_selecionado: return

    item = tabela_livros.item(livro_selecionado)
    livro_id = item['values'][-1]
    print(f'ID do livro selecionado: {livro_id}')
    return livro_id, livro_selecionado

def atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn_add):
    avaliacao_combobox.config(state="normal" if lido_var.get() else "disabled")
    #se estiver vazio enquanto lido for verdadeiro, desabilita o botão de salvar
    if lido_var.get() and not avaliacao_var.get():
        btn_add.config(state="disabled")
    else:
        btn_add.config(state="normal")

