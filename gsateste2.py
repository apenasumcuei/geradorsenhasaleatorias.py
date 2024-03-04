#Utilize python3.9 .\gsateste2.py
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import pyperclip


class GerenciadorSenhas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Senhas")
        self.root.configure(bg="#f0f0f0")  # Mudança de cor de fundo
        self.senhas = self.carregar_senhas()

        self.janela_login = tk.Toplevel()
        self.janela_login.title("Login")
        self.janela_login.configure(bg="#f0f0f0")  # Mudança de cor de fundo
        self.janela_login.attributes("-alpha", 0.95)

        self.rotulo_usuario = tk.Label(self.janela_login, text="Nome de Usuário:", bg="#f0f0f0", fg="green", font=("Helvetica", 12))  # Mudança de fonte
        self.rotulo_usuario.grid(row=0, column=0, padx=5, pady=5)

        self.entrada_usuario = tk.Entry(self.janela_login, font=("Helvetica", 12))  # Mudança de fonte
        self.entrada_usuario.grid(row=0, column=1, padx=5, pady=5)

        self.rotulo_senha = tk.Label(self.janela_login, text="Senha:", bg="#f0f0f0", fg="green", font=("Helvetica", 12))  # Mudança de fonte
        self.rotulo_senha.grid(row=1, column=0, padx=5, pady=5)

        self.entrada_senha = tk.Entry(self.janela_login, show="*", font=("Helvetica", 12))  # Mudança de fonte
        self.entrada_senha.grid(row=1, column=1, padx=5, pady=5)

        self.botao_login = tk.Button(self.janela_login, text="Login", command=self.autenticar_usuario, bg="#007f00", fg="white", font=("Helvetica", 12), bd=0, borderwidth=0, highlightthickness=0)
        self.botao_login.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Esconde a janela principal durante o login
        self.root.withdraw()

    def carregar_senhas(self):
        try:
            with open("senhas.txt", "r") as arquivo:
                senhas = {}
                for linha in arquivo:
                    descricao, senha = linha.strip().split(",")
                    senhas[descricao] = senha
                return senhas
        except FileNotFoundError:
            return {}

    def salvar_senhas(self):
        with open("senhas.txt", "w") as arquivo:
            for descricao, senha in self.senhas.items():
                arquivo.write(f"{descricao},{senha}\n")

    def autenticar_usuario(self):
        usuario_padrao = "admin"
        senha_padrao = "admin"

        usuario_digitado = self.entrada_usuario.get()
        senha_digitada = self.entrada_senha.get()

        if usuario_digitado == usuario_padrao and senha_digitada == senha_padrao:
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.root.deiconify()  # Exibe a janela principal após o login
            self.janela_login.destroy()  # Fecha a janela de login
        else:
            messagebox.showerror("Erro de Login", "Nome de usuário ou senha incorretos.")

    def gerar_senha_aleatoria(self, tamanho):
        import string
        import secrets
        caracteres = string.ascii_letters + string.digits + string.punctuation
        senha_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
        return senha_aleatoria

    def criar_senha_aleatoria(self, tamanho, descricao):
        senha_aleatoria = self.gerar_senha_aleatoria(tamanho)
        self.senhas[descricao] = senha_aleatoria
        messagebox.showinfo("Senha Criada", f"Nova senha criada com sucesso:\nDescrição: {descricao}\nSenha: {senha_aleatoria}")
        self.salvar_senhas()

    def criar_janela_criar_senha(self):
        janela = tk.Toplevel()
        janela.title("Criar Nova Senha")
        janela.configure(bg="#f0f0f0")  # Mudança de cor de fundo
        janela.attributes("-alpha", 0.95)

        rotulo_tamanho = tk.Label(janela, text="Tamanho da Senha:", bg="#f0f0f0", fg="green", font=("Helvetica", 12))  # Mudança de fonte
        rotulo_tamanho.grid(row=0, column=0, padx=5, pady=5)

        entrada_tamanho = tk.Entry(janela, font=("Helvetica", 12))  # Mudança de fonte
        entrada_tamanho.grid(row=0, column=1, padx=5, pady=5)

        rotulo_descricao = tk.Label(janela, text="Descrição:", bg="#f0f0f0", fg="green", font=("Helvetica", 12))  # Mudança de fonte
        rotulo_descricao.grid(row=1, column=0, padx=5, pady=5)

        entrada_descricao = tk.Entry(janela, font=("Helvetica", 12))  # Mudança de fonte
        entrada_descricao.grid(row=1, column=1, padx=5, pady=5)

        botao_criar_senha = tk.Button(janela, text="Criar Senha", command=lambda: self.criar_senha_aleatoria(int(entrada_tamanho.get()), entrada_descricao.get()), bg="#007f00", fg="white", font=("Helvetica", 12), bd=0, borderwidth=0, highlightthickness=0)
        botao_criar_senha.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Posiciona a janela ao lado da janela principal
        self.root.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() + 10
        y = self.root.winfo_y()
        janela.geometry(f"+{x}+{y}")

    def visualizar_senha(self, descricao_selecionada):
        if descricao_selecionada in self.senhas:
            senha = self.senhas[descricao_selecionada]
            pyperclip.copy(senha)  # Copia a senha para a área de transferência
            messagebox.showinfo("Senha", f"A senha para '{descricao_selecionada}' é:\n\n{senha}\n\nCopiado para a área de transferência!")
        else:
            messagebox.showerror("Erro", "Opção inválida. Por favor, escolha novamente.")

    def criar_janela_visualizar_senhas(self):
        if not self.senhas:
            messagebox.showinfo("Senhas", "Não há senhas salvas.")
            return

        def selecionar_senha():
            descricao_selecionada = combo_senhas.get()
            self.visualizar_senha(descricao_selecionada)

        janela = tk.Toplevel()
        janela.title("Visualizar Senhas")
        janela.configure(bg="#f0f0f0")  # Mudança de cor de fundo
        janela.attributes("-alpha", 0.95)

        rotulo_senha = tk.Label(janela, text="Escolha a senha:", bg="#f0f0f0", fg="green", font=("Helvetica", 12))  # Mudança de fonte
        rotulo_senha.grid(row=0, column=0, padx=5, pady=5)

        combo_senhas = ttk.Combobox(janela, values=list(self.senhas.keys()), state="readonly", font=("Helvetica", 12))  # Mudança de fonte
        combo_senhas.grid(row=0, column=1, padx=5, pady=5)

        botao_visualizar = tk.Button(janela, text="Visualizar Senha", command=selecionar_senha, bg="#007f00", fg="white", font=("Helvetica", 12), bd=0, borderwidth=0, highlightthickness=0)
        botao_visualizar.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Posiciona a janela ao lado da janela principal
        self.root.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() + 10
        y = self.root.winfo_y()
        janela.geometry(f"+{x}+{y}")

    def remover_senha(self):
        def confirmar_remocao():
            selecionado = listbox_senhas.curselection()
            if selecionado:
                index = selecionado[0]
                descricao_selecionada = listbox_senhas.get(index)
                if descricao_selecionada in self.senhas:
                    senha = simpledialog.askstring("Confirmação", "Digite sua senha para confirmar a remoção:", show="*")
                    if senha:
                        if senha == "admin":  # Verifique a senha
                            del self.senhas[descricao_selecionada]
                            self.salvar_senhas()
                            messagebox.showinfo("Senha Removida", "A senha foi removida com sucesso.")
                            listbox_senhas.delete(index)
                        else:
                            messagebox.showerror("Erro", "Senha incorreta. A remoção foi cancelada.")
                    else:
                        messagebox.showerror("Erro", "Por favor, digite a senha.")
                else:
                    messagebox.showerror("Erro", f"A senha para '{descricao_selecionada}' não está cadastrada.")
            else:
                messagebox.showerror("Erro", "Por favor, selecione uma senha para remover.")

        janela = tk.Toplevel()
        janela.title("Remover Senha")
        janela.configure(bg="#f0f0f0")  # Mudança de cor de fundo
        janela.attributes("-alpha", 0.95)

        rotulo_senhas = tk.Label(janela, text="Senhas:", bg="#f0f0f0", fg="green", font=("Helvetica", 12))  # Mudança de fonte
        rotulo_senhas.grid(row=0, column=0, padx=5, pady=5)

        listbox_senhas = tk.Listbox(janela, font=("Helvetica", 12), selectmode="SINGLE")
        for descricao in self.senhas.keys():
            listbox_senhas.insert(tk.END, descricao)
        listbox_senhas.grid(row=0, column=1, padx=5, pady=5)

        botao_remover = tk.Button(janela, text="Remover Senha", command=confirmar_remocao, bg="#007f00", fg="white", font=("Helvetica", 12), bd=0, borderwidth=0, highlightthickness=0)
        botao_remover.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Posiciona a janela ao lado da janela principal
        self.root.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() + 10
        y = self.root.winfo_y()
        janela.geometry(f"+{x}+{y}")

    def editar_senha(self):
        def confirmar_edicao():
            selecionado = listbox_senhas.curselection()
            if selecionado:
                index = selecionado[0]
                descricao_selecionada = listbox_senhas.get(index)
                if descricao_selecionada in self.senhas:
                    nova_descricao = entrada_nova_descricao.get()
                    if nova_descricao:
                        self.senhas[nova_descricao] = self.senhas.pop(descricao_selecionada)
                        self.salvar_senhas()
                        messagebox.showinfo("Senha Editada", "A senha foi editada com sucesso.")
                        janela.destroy()
                    else:
                        messagebox.showerror("Erro", "Por favor, digite uma nova descrição.")
                else:
                    messagebox.showerror("Erro", f"A senha para '{descricao_selecionada}' não está cadastrada.")
            else:
                messagebox.showerror("Erro", "Por favor, selecione uma senha para editar.")

        janela = tk.Toplevel()
        janela.title("Editar Senha")
        janela.configure(bg="#f0f0f0")  # Mudança de cor de fundo
        janela.attributes("-alpha", 0.95)

        rotulo_senhas = tk.Label(janela, text="Senhas:", bg="#f0f0f0", fg="green", font=("Helvetica", 12))  # Mudança de fonte
        rotulo_senhas.grid(row=0, column=0, padx=5, pady=5)

        listbox_senhas = tk.Listbox(janela, font=("Helvetica", 12), selectmode="SINGLE")
        for descricao in self.senhas.keys():
            listbox_senhas.insert(tk.END, descricao)
        listbox_senhas.grid(row=0, column=1, padx=5, pady=5)

        rotulo_nova_descricao = tk.Label(janela, text="Nova Descrição:", bg="#f0f0f0", fg="green", font=("Helvetica", 12))  # Mudança de fonte
        rotulo_nova_descricao.grid(row=1, column=0, padx=5, pady=5)

        entrada_nova_descricao = tk.Entry(janela, font=("Helvetica", 12))  # Mudança de fonte
        entrada_nova_descricao.grid(row=1, column=1, padx=5, pady=5)

        botao_editar = tk.Button(janela, text="Confirmar Edição", command=confirmar_edicao, bg="#007f00", fg="white", font=("Helvetica", 12), bd=0, borderwidth=0, highlightthickness=0)
        botao_editar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Posiciona a janela ao lado da janela principal
        self.root.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() + 10
        y = self.root.winfo_y()
        janela.geometry(f"+{x}+{y}")

    def main(self):
        botao_criar_senha = tk.Button(self.root, text="Criar Nova Senha", command=self.criar_janela_criar_senha, bg="#007f00", fg="white", font=("Helvetica", 14), bd=0, borderwidth=0, highlightthickness=0)
        botao_criar_senha.pack(padx=10, pady=5)

        botao_visualizar_senhas = tk.Button(self.root, text="Visualizar Senhas", command=self.criar_janela_visualizar_senhas, bg="#007f00", fg="white", font=("Helvetica", 14), bd=0, borderwidth=0, highlightthickness=0)
        botao_visualizar_senhas.pack(padx=10, pady=5)

        botao_editar_senha = tk.Button(self.root, text="Editar Senha", command=self.editar_senha, bg="#007f00", fg="white", font=("Helvetica", 14), bd=0, borderwidth=0, highlightthickness=0)
        botao_editar_senha.pack(padx=10, pady=5)

        botao_remover_senha = tk.Button(self.root, text="Remover Senha", command=self.remover_senha, bg="#007f00", fg="white", font=("Helvetica", 14), bd=0, borderwidth=0, highlightthickness=0)
        botao_remover_senha.pack(padx=10, pady=5)

        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorSenhas(root)
    app.main()
