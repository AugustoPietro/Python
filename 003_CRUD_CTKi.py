import customtkinter as ctki
import sqlite3 as sql

# Criar base de dados
def db_register():
    # product_id é do tipo auto increment
    product_name    = entry_name.get()
    product_cost    = entry_cost.get()
    product_amount  = entry_amount.get()

    # Banco de Dados
    db_connect = sql.connect('produtos.db')

    # Criar um cursor para executar comandos SQL
    db_cursor = db_connect.cursor()

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS produtos
                    (idproduto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome STRING,
                    valorCusto INTEGER,
                    quantidade INTEGER)''')

    # Inserir os valores no banco de dados
    db_cursor.execute('INSERT INTO produtos (nome, valorCusto, quantidade) VALUES (?, ?, ?)',
                   (product_name, product_cost, product_amount))

    # Confirmação no terminal
    print('Registro efetuado com sucesso.')
   
    # Salvar as alterações
    db_connect.commit()

    # Fechar a conexão
    db_connect.close()

def db_show_data():
    # Limpar a tabela antiga
    for widget in frame_read.winfo_children():
        widget.destroy()

    # Conectar ao banco de dados
    db_connect  = sql.connect('produtos.db')
    db_cursor   = db_connect.cursor()

    # Selecionar todos os registros da tabela
    db_cursor.execute('SELECT * FROM produtos')
    rows = db_cursor.fetchall()

    # Criar uma tabela para exibir os dados
    table = ctki.CTkFrame(frame_read,  fg_color='lightslategray', corner_radius=3)
    table.grid(row=5, column=1, columnspan=2, padx=20, pady=10)
    
    # Cabeçalho da tabela
    header = ['ID', 'Nome', 'Valor', 'Quantidade']
    for i, coluna in enumerate(header):
        label = ctki.CTkLabel(table, text=coluna, width=60, font=('Candara Bold', 14))
        label.grid(row=0, column=i)

    # Dados da tabela
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            entry = ctki.CTkEntry(table, width=80, border_width=1, corner_radius=3, font=('Candara', 14))
            entry.insert(ctki.END, str(value))
            entry.grid(row=i+1, column=j)            
            entry.configure(cursor='hand2', state='readonly')
            entry.bind('<Button-1>', lambda event, id=row[0]: on_table_click(id)) # Controle de evento no click do botão esquerdo (Button-1)

    # Fechar a conexão com o banco de dados
    db_connect.close()

def on_table_click(product_id):
    # Conectar ao banco de dados
    db_connect = sql.connect('produtos.db')
    db_cursor = db_connect.cursor()

    # Selecionar o registro com base no ID do produto
    db_cursor.execute('SELECT nome, valorCusto, quantidade FROM produtos WHERE idproduto = ?', (product_id,))
    row = db_cursor.fetchone()  # Recupere a linha correspondente ao ID do produto

    if row:
        product_name, product_cost, product_amount = row

        # Preencher os campos de entrada com as informações do banco de dados
        entry_id.delete(0, ctki.END)
        entry_id.insert(ctki.END, str(product_id))

        entry_name.delete(0, ctki.END)
        entry_name.insert(ctki.END, product_name)

        entry_cost.delete(0, ctki.END)
        entry_cost.insert(ctki.END, str(product_cost))

        entry_amount.delete(0, ctki.END)
        entry_amount.insert(ctki.END, str(product_amount))

    # Fechar a conexão com o banco de dados
    db_connect.close()  
   
def db_update():
    # Obter os valores digitados nos campos de entrada
    product_id      = entry_id.get()
    product_name    = entry_name.get()
    product_cost    = entry_cost.get()
    product_amount  = entry_amount.get()

    # Conectar ao banco de dados
    db_connect  = sql.connect('produtos.db')
    db_cursor   = db_connect.cursor()

    # Atualizar os valores no banco de dados
    db_cursor.execute('UPDATE produtos SET nome = ?, valorCusto = ?, quantidade = ? WHERE idproduto = ?',
                 (product_name, product_cost, product_amount, product_id))

    # Confirmação no terminal
    print('Atualizado com sucesso.')

    # Salvar as alterações e fechar a conexão com o banco de dados
    db_connect.commit()
    db_connect.close()

    # Limpar os campos de entrada
    entry_id.delete(0, ctki.END)
    entry_name.delete(0, ctki.END)
    entry_cost.delete(0, ctki.END)
    entry_amount.delete(0, ctki.END)

def db_delete():
    # Obter o nome do registro a ser excluído
    product_id  = entry_id.get()

    # Conectar ao banco de dados
    db_connect  = sql.connect('produtos.db')
    db_cursor   = db_connect.cursor()

    # Excluir o registro do banco de dados
    db_cursor.execute('DELETE FROM produtos WHERE idproduto = ?', (product_id))

    # Confirmação no terminal
    print('Excluido com sucesso.')

    # Salvar as alterações e fechar a conexão com o banco de dados
    db_connect.commit()
    db_connect.close()

    # Limpar os campos de entrada
    entry_id.delete(0, ctki.END)
    entry_name.delete(0, ctki.END)
    entry_cost.delete(0, ctki.END)
    entry_amount.delete(0, ctki.END)

# Interface
janela = ctki.CTk(fg_color='darkslategray')

janela.title('Cadastro de Produtos')
janela.geometry('1024x768')
janela.resizable(width=True, height=True)
janela.minsize(800,600)

frame_left = ctki.CTkFrame(janela, fg_color='slategray', corner_radius=3)
frame_left.pack(side='left', padx=0, pady=0, fill='both', expand=0)

frame_write = ctki.CTkFrame(frame_left, fg_color='lightslategray', corner_radius=10)
frame_write.pack(side='left', padx=5, pady=5)

frame_right = ctki.CTkFrame(janela, fg_color='slategray', corner_radius=3)
frame_right.pack(side='right', padx=0, pady=0, fill='both', expand=0)

frame_read = ctki.CTkFrame(frame_right, fg_color='lightslategray', corner_radius=10)
frame_read.pack(side='right', padx=5, pady=5)

# Campos de entrada
label_id = ctki.CTkLabel(master=frame_write, width=100, height=20, text='ID Produto', text_color='white', font=('Candara Bold', 14))
label_id.grid(row=0, column=0, padx=20, pady=10)

label_name = ctki.CTkLabel(master=frame_write, width=100, height=20, text='Nome', text_color='white', font=('Candara Bold', 14))
label_name.grid(row=1, column=0, padx=20, pady=10)

label_cost = ctki.CTkLabel(master=frame_write, width=100, height=20, text='Valor Custo', text_color='white', font=('Candara Bold', 14))
label_cost.grid(row=2, column=0, padx=20, pady=10)

label_amount = ctki.CTkLabel(master=frame_write, width=100, height=20, text='Quantidade', text_color='white', font=('Candara Bold', 14))
label_amount.grid(row=3, column=0, padx=20, pady=10)

entry_id = ctki.CTkEntry(master=frame_write, width=150, height=20, border_width=1, corner_radius=10, placeholder_text='Código do Produto', state='normal')
entry_id.grid(row=0, column=1, padx=20, pady=10)

entry_name = ctki.CTkEntry(master=frame_write, width=150, height=20, border_width=1, corner_radius=10, placeholder_text='Nome do Produto')
entry_name.grid(row=1, column=1, padx=20, pady=10)

entry_cost = ctki.CTkEntry(master=frame_write, width=150, height=20, border_width=1, corner_radius=10, placeholder_text='Custo do Produto')
entry_cost.grid(row=2, column=1, padx=20, pady=10)

entry_amount = ctki.CTkEntry(master=frame_write, width=150, height=20, border_width=1, corner_radius=10, placeholder_text='Qtde de Produtos')
entry_amount.grid(row=3, column=1, padx=20, pady=10)

# Botões
btn_register = ctki.CTkButton(master=frame_write, text='Inserir', width=80, font=('Candara Bold', 14), fg_color='slategray', hover_color='darkslategray', border_color='darkslategray', border_width=1.5, corner_radius=15, command=db_register)
btn_register.grid(row=0, column=2, columnspan=2, padx=20, pady=10)

btn_update = ctki.CTkButton(master=frame_write, text='Alterar', width=80, font=('Candara Bold', 14), fg_color='slategray', hover_color='darkslategray', border_color='darkslategray', border_width=1.5, corner_radius=15, command=db_update)
btn_update.grid(row=1, column=2, columnspan=2, padx=20, pady=10)

btn_show_data = ctki.CTkButton(master=frame_write, text='Mostrar', width=80, font=('Candara Bold', 14), fg_color='slategray', hover_color='darkslategray', border_color='darkslategray', border_width=1.5, corner_radius=15, command=db_show_data)
btn_show_data.grid(row=2, column=2, columnspan=2, padx=20, pady=10)

btn_delete = ctki.CTkButton(master=frame_write, text='Excluir', width=80, font=('Candara Bold', 14), fg_color='slategray', hover_color='darkred', border_color='darkred', border_width=1.5, corner_radius=15, command=db_delete)
btn_delete.grid(row=3, column=2, columnspan=2, padx=20, pady=10)
    
# Janela em loop
janela.mainloop()