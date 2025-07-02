import sqlite3 # banco de dados
import tkinter as tk # interface basica
from tkinter import messagebox # caixas de mensagens
from tkinter import ttk # interface grafica tb

def conectar():
    return sqlite3.connect('teste.db')
# criar o banco (connect)

def criar_tabela():
    conn = conectar()
    c= conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
        nome TEXT NOT NULL,
        idade TEXT NOT NULL,
        peso real NOT NULL,
        altura real NOT NULL,            
        imc integer NOT NULL                    
        )       
    ''')
    conn.commit()
    conn.close()
  


# CREATE
def inserir_usuario():
    nome = entry_nome.get()
    idade = entry_idade.get()
    peso = float (entry_peso.get())
    altura = float( entry_altura.get())
    imc = peso /(altura **2) 

    if nome and idade and peso and altura:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO usuarios(nome, idade, peso, altura,imc) VALUES(?,?,?,?,?)', (nome, idade, peso, altura,imc))
        conn.commit()
        conn.close()
        messagebox.showinfo('AVISO', 'DADOS INSERIDOS COM SUCESSO!') 
        mostrar_usuario()
    else:
        messagebox.showerror('ERRO', 'ALGO DEU ERRADO!') 

# READ
def mostrar_usuario():
    for row in tree.get_children():   
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()    
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()
    for usuario in usuarios:
        tree.insert("", "end", values=(usuario[0], usuario[1],usuario[2],usuario[3],usuario[4]))
    conn.close()    


# DELETE
def delete_usuario():
    dado_del = tree.selection()
    if dado_del:
       user_id = tree.item(dado_del)['values'][0]
       conn = conectar()
       c = conn.cursor()    
       c.execute('DELETE FROM usuarios WHERE nome = ? ',(user_id,))
       conn.commit()
       conn.close()
       messagebox.showinfo('', 'DADO DELETADO')
       mostrar_usuario()

    else:
       messagebox.showerror('', 'OCORREU UM ERRO')  

# UPDATE 
       
def editar():
     selecao = tree.selection()
     if selecao:
         user_id = tree.item(selecao)['values'][0]
         novo_nome = entry_nome.get()
         novo_idade = entry_idade.get()
         novo_peso = entry_peso.get()
         novo_altura = entry_altura.get()        

         if novo_nome and novo_idade and novo_peso and novo_altura:
            conn = conectar()
            c = conn.cursor()    
            c.execute('UPDATE usuarios SET nome = ? , idade = ? , peso = ?, altura = ? WHERE nome = ? ',(novo_nome,novo_idade,novo_peso,novo_altura,user_id))
            conn.commit()
            conn.close()  
            messagebox.showinfo('', 'DADOS ATUALIZADOS')
            mostrar_usuario()

         else:
             messagebox.showwarning('', 'PREENCHA TODOS OS CAMPOS')

     else:
            messagebox.showerror('','ALGO DEU ERRADO!')


# VAMOS COMPLETAR A INTERFACE GRÁFICA...
# 1
janela = tk.Tk()
janela.title('SAÚDE & BEM-ESTAR')

label_nome = tk.Label(janela, text='NOME:')
label_nome.grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_idade = tk.Label(janela, text='IDADE:')
label_idade.grid(row=1, column=0, padx=10, pady=10)
entry_idade = tk.Entry(janela)
entry_idade.grid(row=1, column=1, padx=10, pady=10)

label_peso = tk.Label(janela, text='PESO:')
label_peso.grid(row=2, column=0, padx=10, pady=10)
entry_peso = tk.Entry(janela)
entry_peso.grid(row=2, column=1, padx=10, pady=10)

label_altura = tk.Label(janela, text='ALTURA:')
label_altura.grid(row=3, column=0, padx=10, pady=10)
entry_altura = tk.Entry(janela)
entry_altura.grid(row=3, column=1, padx=10, pady=10)


label_peso = tk.Label(janela, text='PESO:')
label_peso.grid(row=2, column=0, padx=10, pady=10)

entry_peso = tk.Entry(janela, text='PESO:')
entry_peso.grid(row=2, column=1, padx=10, pady=10)



# botões

btn_salvar = tk.Button(janela, text='SALVAR',command=inserir_usuario)
btn_salvar.grid(row = 4, column=0, padx=10, pady=10  )

btn_deletar = tk.Button(janela, text='DELETAR',command=delete_usuario)
btn_deletar.grid(row = 4, column=1, padx=10, pady=10  )

btn_atualizar = tk.Button(janela, text='ATUALIZAR',command=editar)
btn_atualizar.grid(row = 4, column=2, padx=10, pady=10  )

# arvore
columns = ('NOME', 'IDADE','PESO','ALTURA','IMC')

tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=6, column=0,columnspan=2, padx=10, pady=10 )

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_usuario()


janela.mainloop()