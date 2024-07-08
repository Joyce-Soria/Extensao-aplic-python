import tkinter as tk
from tkinter import messagebox
import sqlite3

class CondominioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Moradores")
        
        # Aumenta o tamanho da janela principal
        self.root.geometry("700x400")
        
        self.create_widgets()
        self.create_database()
        self.populate_listbox()
        
    def create_widgets(self):
        # Labels and Entry widgets
        self.label_nome = tk.Label(self.root, text="Nome")
        self.label_nome.grid(row=0, column=0, padx=10, pady=10)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)
        
        self.label_apartamento = tk.Label(self.root, text="Apartamento")
        self.label_apartamento.grid(row=1, column=0, padx=10, pady=10)
        self.entry_apartamento = tk.Entry(self.root)
        self.entry_apartamento.grid(row=1, column=1, padx=10, pady=10)
        
        self.label_telefone = tk.Label(self.root, text="Telefone")
        self.label_telefone.grid(row=2, column=0, padx=10, pady=10)
        self.entry_telefone = tk.Entry(self.root)
        self.entry_telefone.grid(row=2, column=1, padx=10, pady=10)
        
        # Campo de pesquisa
        self.label_search = tk.Label(self.root, text="Pesquisar")
        self.label_search.grid(row=3, column=0, padx=10, pady=10)
        self.entry_search = tk.Entry(self.root)
        self.entry_search.grid(row=3, column=1, padx=10, pady=10)
        
        self.btn_search = tk.Button(self.root, text="Buscar", command=self.search_morador)
        self.btn_search.grid(row=3, column=2, padx=10, pady=10)
        
        # Listbox to display moradores with a scrollbar
        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.grid(row=0, column=3, rowspan=6, padx=10, pady=10)
        
        self.scrollbar = tk.Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(self.listbox_frame, yscrollcommand=self.scrollbar.set, width=50)
        self.listbox.pack()
        self.scrollbar.config(command=self.listbox.yview)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # Buttons
        self.btn_add = tk.Button(self.root, text="Adicionar", command=self.add_morador)
        self.btn_add.grid(row=4, column=0, padx=10, pady=10)
        
        self.btn_edit = tk.Button(self.root, text="Editar", command=self.edit_morador)
        self.btn_edit.grid(row=4, column=1, padx=10, pady=10)
        
        self.btn_delete = tk.Button(self.root, text="Excluir", command=self.delete_morador)
        self.btn_delete.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        
        self.btn_save = tk.Button(self.root, text="Salvar", command=self.save_morador)
        self.btn_save.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    
    def create_database(self):
        conn = sqlite3.connect('condominio.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS moradores
                          (id INTEGER PRIMARY KEY,
                           nome TEXT,
                           apartamento TEXT,
                           telefone TEXT)''')
        conn.commit()
        conn.close()
    
    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        conn = sqlite3.connect('condominio.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM moradores")
        rows = cursor.fetchall()
        for row in rows:
            display_text = f"ID: {row[0]}, Nome: {row[1]}, Apartamento: {row[2]}, Telefone: {row[3]}"
            self.listbox.insert(tk.END, display_text)
        conn.close()
    
    def on_select(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        selected_text = self.listbox.get(index)
        
        # Extrai as informações do texto exibido na listbox
        id_str, nome_str, apto_str, tel_str = selected_text.split(", ")
        self.morador_id = int(id_str.split(": ")[1])
        
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(tk.END, nome_str.split(": ")[1])
        
        self.entry_apartamento.delete(0, tk.END)
        self.entry_apartamento.insert(tk.END, apto_str.split(": ")[1])
        
        self.entry_telefone.delete(0, tk.END)
        self.entry_telefone.insert(tk.END, tel_str.split(": ")[1])
    
    def add_morador(self):
        nome = self.entry_nome.get()
        apartamento = self.entry_apartamento.get()
        telefone = self.entry_telefone.get()
        
        if not nome or not apartamento or not telefone:
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios")
            return
        
        conn = sqlite3.connect('condominio.db')
        cursor = conn.cursor()
        
        # Verifica se já existem 5 moradores no apartamento
        cursor.execute("SELECT COUNT(*) FROM moradores WHERE apartamento=?", (apartamento,))
        count = cursor.fetchone()[0]
        if count >= 5:
            messagebox.showwarning("Erro", "Já existem 5 moradores nesse apartamento")
            conn.close()
            return
        
        cursor.execute("INSERT INTO moradores (nome, apartamento, telefone) VALUES (?, ?, ?)", 
                       (nome, apartamento, telefone))
        conn.commit()
        conn.close()
        
        self.populate_listbox()
        self.clear_entries()
    
    def edit_morador(self):
        if not self.listbox.curselection():
            messagebox.showwarning("Erro", "Selecione um morador para editar")
            return
        
        index = self.listbox.curselection()[0]
        selected_text = self.listbox.get(index)
        
        id_str, nome_str, apto_str, tel_str = selected_text.split(", ")
        self.morador_id = int(id_str.split(": ")[1])
        
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(tk.END, nome_str.split(": ")[1])
        
        self.entry_apartamento.delete(0, tk.END)
        self.entry_apartamento.insert(tk.END, apto_str.split(": ")[1])
        
        self.entry_telefone.delete(0, tk.END)
        self.entry_telefone.insert(tk.END, tel_str.split(": ")[1])
    
    def save_morador(self):
        if not hasattr(self, 'morador_id'):
            messagebox.showwarning("Erro", "Selecione um morador para salvar")
            return
        
        nome = self.entry_nome.get()
        apartamento = self.entry_apartamento.get()
        telefone = self.entry_telefone.get()
        
        if not nome or not apartamento or not telefone:
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios")
            return
        
        conn = sqlite3.connect('condominio.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE moradores SET nome=?, apartamento=?, telefone=? WHERE id=?", 
                       (nome, apartamento, telefone, self.morador_id))
        conn.commit()
        conn.close()
        
        self.populate_listbox()
        self.clear_entries()
    
    def delete_morador(self):
        if not self.listbox.curselection():
            messagebox.showwarning("Erro", "Selecione um morador para excluir")
            return
        
        index = self.listbox.curselection()[0]
        selected_text = self.listbox.get(index)
        
        id_str, nome_str, apto_str, tel_str = selected_text.split(", ")
        morador_id = int(id_str.split(": ")[1])
        
        conn = sqlite3.connect('condominio.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM moradores WHERE id=?", (morador_id,))
        conn.commit()
        conn.close()
        
        self.populate_listbox()
        self.clear_entries()
    
    def search_morador(self):
        search_term = self.entry_search.get()
        if not search_term:
            messagebox.showwarning("Erro", "Digite um termo de pesquisa")
            return
        
        self.listbox.delete(0, tk.END)
        conn = sqlite3.connect('condominio.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM moradores WHERE nome LIKE ? OR apartamento LIKE ? OR telefone LIKE ?", 
                       (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        rows = cursor.fetchall()
        for row in rows:
            display_text = f"ID: {row[0]}, Nome: {row[1]}, Apartamento: {row[2]}, Telefone: {row[3]}"
            self.listbox.insert(tk.END, display_text)
        conn.close()
    
    def clear_entries(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_apartamento.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        if hasattr(self, 'morador_id'):
            del self.morador_id

if __name__ == "__main__":
    root = tk.Tk()
    app = CondominioApp(root)
    root.mainloop()
