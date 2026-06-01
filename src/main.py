import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from persistencia import FICHEIROS
from clube import criar_clube, listar_clubes, remover_clube
from jogador import criar_jogador, listar_jogadores, remover_jogador
from treinador import criar_treinador, listar_treinadores, remover_treinador
from jogo import criar_jogo, listar_jogos, remover_jogo


class FootballManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏆 Football Manager - Sistema de Gestão")
        self.root.geometry("1250x780")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.criar_aba_clubes()
        self.criar_aba_jogadores()
        self.criar_aba_treinadores()
        self.criar_aba_jogos()

    # ====================== CLUBES ======================
    def criar_aba_clubes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Clubes")
        self.tree_clubes = self.criar_treeview(frame, ["ID", "Nome", "NIF"])
        self.adicionar_botoes(frame, self.atualizar_clubes, self.janela_novo_clube, self.remover_clube)
        self.atualizar_clubes()

    def atualizar_clubes(self):
        self.atualizar_tree(self.tree_clubes, listar_clubes(), ["nome", "nif"])

    def janela_novo_clube(self):
        self.janela_form("Novo Clube", ["Nome", "NIF"], criar_clube, self.atualizar_clubes)

    def remover_clube(self):
        self.remover_item(self.tree_clubes, remover_clube, self.atualizar_clubes)

    # ====================== JOGADORES ======================
    def criar_aba_jogadores(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Jogadores")
        self.tree_jogadores = self.criar_treeview(frame, ["ID", "Nome", "Idade", "Posição", "Camisola", "Salário"])
        self.adicionar_botoes(frame, self.atualizar_jogadores, self.janela_novo_jogador, self.remover_jogador)
        self.atualizar_jogadores()

    def atualizar_jogadores(self):
        jogadores = listar_jogadores()
        for item in self.tree_jogadores.get_children():
            self.tree_jogadores.delete(item)
        for id_j, j in jogadores.items():
            self.tree_jogadores.insert("", "end", values=(
                id_j, j["nome"], j.get("idade", "-"), j["posicao"],
                j["numero_camisa"], f"{float(j['salario']):.2f}€"
            ))

    def janela_novo_jogador(self):
        win = tk.Toplevel(self.root)
        win.title("Novo Jogador")
        win.geometry("520x580")

        entries = {}
        labels = ["Nome", "Data Nascimento (YYYY-MM-DD)", "Número Camisola", "Salário"]
        for label in labels:
            tk.Label(win, text=label + ":", font=("Arial", 10)).pack(pady=8, anchor="w", padx=40)
            entry = tk.Entry(win, width=50)
            entry.pack(pady=5)
            entries[label] = entry

        tk.Label(win, text="Posição:", font=("Arial", 10)).pack(pady=8, anchor="w", padx=40)
        pos_combo = ttk.Combobox(win, values=["guarda-redes", "defesa", "médio", "avançado"], width=47)
        pos_combo.pack(pady=5)

        def salvar():
            try:
                sucesso, msg = criar_jogador(
                    entries["Nome"].get(),
                    entries["Data Nascimento (YYYY-MM-DD)"].get(),
                    int(entries["Número Camisola"].get()),
                    pos_combo.get(),
                    float(entries["Salário"].get())
                )
                if sucesso:
                    messagebox.showinfo("Sucesso", "Jogador criado com sucesso!")
                    win.destroy()
                    self.atualizar_jogadores()
                else:
                    messagebox.showerror("Erro", msg)
            except Exception as e:
                messagebox.showerror("Erro", f"Verifique os campos numéricos!\n{e}")

        ttk.Button(win, text="💾 Guardar Jogador", command=salvar).pack(pady=25)

    def remover_jogador(self):
        self.remover_item(self.tree_jogadores, remover_jogador, self.atualizar_jogadores)

    # ====================== TREINADORES ======================
    def criar_aba_treinadores(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Treinadores")
        self.tree_treinadores = self.criar_treeview(frame, ["ID", "Nome", "Nacionalidade", "Licença", "Clube"])
        self.adicionar_botoes(frame, self.atualizar_treinadores, self.janela_novo_treinador, self.remover_treinador)
        self.atualizar_treinadores()

    def atualizar_treinadores(self):
        treinadores = listar_treinadores()
        for item in self.tree_treinadores.get_children():
            self.tree_treinadores.delete(item)
        for id_t, t in treinadores.items():
            self.tree_treinadores.insert("", "end", values=(
                id_t, t["nome"], t["nacionalidade"], t["licenca_UEFA"], t.get("id_clube", "Sem clube")
            ))

    def janela_novo_treinador(self):
        win = tk.Toplevel(self.root)
        win.title("Novo Treinador")
        win.geometry("520x520")

        entries = {}
        labels = ["Nome", "Nacionalidade", "Data Nascimento (YYYY-MM-DD)", "Licença UEFA (A/B/PRO)"]
        for label in labels:
            tk.Label(win, text=label + ":", font=("Arial", 10)).pack(pady=8, anchor="w", padx=40)
            entry = tk.Entry(win, width=50)
            entry.pack(pady=5)
            entries[label] = entry

        def salvar():
            try:
                sucesso, msg = criar_treinador(
                    entries["Nome"].get(),
                    entries["Nacionalidade"].get(),
                    entries["Data Nascimento (YYYY-MM-DD)"].get(),
                    entries["Licença UEFA (A/B/PRO)"].get()
                )
                if sucesso:
                    messagebox.showinfo("Sucesso", "Treinador criado com sucesso!")
                    win.destroy()
                    self.atualizar_treinadores()
                else:
                    messagebox.showerror("Erro", msg)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")

        ttk.Button(win, text="💾 Guardar Treinador", command=salvar).pack(pady=25)

    def remover_treinador(self):
        self.remover_item(self.tree_treinadores, remover_treinador, self.atualizar_treinadores)

    # ====================== JOGOS ======================
    def criar_aba_jogos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Jogos")
        self.tree_jogos = self.criar_treeview(frame, ["ID", "Data", "Estádio", "Casa", "Fora", "Resultado"])
        self.adicionar_botoes(frame, self.atualizar_jogos, self.janela_novo_jogo, self.remover_jogo)
        self.atualizar_jogos()

    def atualizar_jogos(self):
        jogos = listar_jogos()
        for item in self.tree_jogos.get_children():
            self.tree_jogos.delete(item)
        for id_j, j in jogos.items():
            self.tree_jogos.insert("", "end", values=(
                id_j, j["data"], j["estadio"], j["id_clube_casa"],
                j["id_clube_fora"], f"{j['golos_casa']}-{j['golos_fora']}"
            ))

    def janela_novo_jogo(self):
        win = tk.Toplevel(self.root)
        win.title("Novo Jogo")
        win.geometry("520x520")

        entries = {}
        labels = ["Data (YYYY-MM-DD)", "Estádio", "ID Clube Casa", "ID Clube Fora", "Golos Casa", "Golos Fora"]
        for label in labels:
            tk.Label(win, text=label + ":").pack(pady=8, anchor="w", padx=40)
            entry = tk.Entry(win, width=50)
            entry.pack(pady=5)
            entries[label] = entry

        def salvar():
            try:
                sucesso, msg = criar_jogo(
                    entries["Data (YYYY-MM-DD)"].get(),
                    entries["Estádio"].get(),
                    int(entries["ID Clube Casa"].get()),
                    int(entries["ID Clube Fora"].get()),
                    int(entries["Golos Casa"].get() or 0),
                    int(entries["Golos Fora"].get() or 0)
                )
                if sucesso:
                    messagebox.showinfo("Sucesso", "Jogo criado com sucesso!")
                    win.destroy()
                    self.atualizar_jogos()
                else:
                    messagebox.showerror("Erro", msg)
            except Exception as e:
                messagebox.showerror("Erro", f"Verifique os IDs e números!\n{e}")

        ttk.Button(win, text="💾 Guardar Jogo", command=salvar).pack(pady=25)

    def remover_jogo(self):
        self.remover_item(self.tree_jogos, remover_jogo, self.atualizar_jogos)

    # ====================== FUNÇÕES AUXILIARES ======================
    def criar_treeview(self, parent, colunas):
        tree = ttk.Treeview(parent, columns=colunas, show="headings")
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")
        tree.pack(fill="both", expand=True, pady=10)
        return tree

    def adicionar_botoes(self, parent, atualizar_cmd, novo_cmd, remover_cmd=None):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=8)
        ttk.Button(frame, text="🔄 Atualizar", command=atualizar_cmd).pack(side="left", padx=5)
        ttk.Button(frame, text="➕ Novo", command=novo_cmd).pack(side="left", padx=5)
        if remover_cmd:
            ttk.Button(frame, text="🗑 Remover", command=remover_cmd).pack(side="left", padx=5)

    def atualizar_tree(self, tree, dados, campos):
        for item in tree.get_children():
            tree.delete(item)
        for id_item, item in dados.items():
            valores = [id_item] + [item.get(campo, "") for campo in campos]
            tree.insert("", "end", values=valores)

    def remover_item(self, tree, funcao_remover, atualizar_func):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um item!")
            return
        id_item = tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar Remoção", f"Remover item ID {id_item}?"):
            sucesso, msg = funcao_remover(str(id_item))
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                atualizar_func()
            else:
                messagebox.showerror("Erro", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = FootballManagerApp(root)
    root.mainloop()
