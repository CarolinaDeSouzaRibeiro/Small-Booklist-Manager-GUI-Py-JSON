def get_livro_from_table_selection(tabela_livros):
    '''Recebe uma tabela tkinter tree com livros
    Se um elemento estiver selecionado, retorna o ID e a seleção do livro'''
    #pega a coluna selecionada na tabela
    try:
        livro_selecionado = tabela_livros.selection()
        item = tabela_livros.item(livro_selecionado)
        livro_id = item['values'][-1]
        print(f'ID do livro selecionado: {livro_id}')
        return livro_id, livro_selecionado
    except:
        print("Erro ao obter livro da seleção da tabela.\nCertifique-se de que um livro esteja selecionado.")
        #TODO: Inform user (GUI window)
        return None, None


def atualizar_estado_combobox(avaliacao_combobox, lido_var, avaliacao_var, btn):
    '''Modifica estado da combobox de avaliação e do botão de salvar com base na avaliação e se o livro foi lido ou não

    Impede acesso ao combobox caso o livro não tenha sido marcado como lido.
    Impede acesso ao botão caso o livro tenha sido marcado como lido, mas nenhuma avaliação foi selecionada.
    '''
    #estado combobox
    # estado_combobox = "normal" if lido_var.get() else "disabled"
    # estado_btn = "normal" if lido_var.get() and avaliacao_var.get() else "disabled"
    print(f'Avaliado. {avaliacao_var.get()}/5') if avaliacao_var.get() else print("Não avaliado.")
    print ('Lido') if lido_var.get() else print("Não lido.")

    estado_combo = "disabled" if not lido_var.get() else "normal"
    estado_btn = "disabled" if lido_var.get() and not avaliacao_var.get() else "normal"
    print(f"Estado do botão:{estado_btn}\nEstado do combobox:{estado_combo}\n")

    avaliacao_combobox.config(state=estado_combo)
    btn.config(state=estado_btn)

