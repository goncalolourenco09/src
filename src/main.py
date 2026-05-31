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
        self.root.geometry("1200x750")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.criar_aba_clubes()
        self.criar_aba_jogadores()
        self.criar_aba_treinadores()
        self.criar_aba_jogos()

    # ==================== CLUBES ====================
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

    # ==================== JOGADORES ====================
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
                id_j, j["nome"], j.get("idade"), j["posicao"], j["numero_camisa"], f"{j['salario']:.2f}€"
            ))

    def janela_novo_jogador(self):
        win = tk.Toplevel(self.root)
        win.title("Novo Jogador")
        win.geometry("500x550")

        entries = {}
        labels = ["Nome", "Data Nascimento (YYYY-MM-DD)", "Número Camisola", "Salário"]
        for label in labels:
            tk.Label(win, text=label + ":").pack(pady=8, anchor="w", padx=30)
            entry = tk.Entry(win, width=50)
            entry.pack(pady=5)
            entries[label] = entry

        tk.Label(win, text="Posição:").pack(pady=8, anchor="w", padx=30)
        pos = ttk.Combobox(win, values=["guarda-redes", "defesa", "médio", "avançado"], width=47)
        pos.pack(pady=5)

        def salvar():
            try:
                sucesso, msg = criar_jogador(
                    entries["Nome"].get(),
                    entries["Data Nascimento (YYYY-MM-DD)"].get(),
                    int(entries["Número Camisola"].get()),
                    pos.get(),
                    float(entries["Salário"].get())
                )
                if sucesso:
                    messagebox.showinfo("Sucesso", "Jogador criado!")
                    win.destroy()
                    self.atualizar_jogadores()
                else:
                    messagebox.showerror("Erro", msg)
            except:
                messagebox.showerror("Erro", "Verifique os dados numéricos")

        ttk.Button(win, text="Guardar Jogador", command=salvar).pack(pady=20)

    # ==================== TREINADORES ====================
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
        # Similar ao de jogador - podes expandir
        messagebox.showinfo("Info", "Janela de Treinador pronta para implementar")

    # ==================== JOGOS ====================
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
                id_j, j["data"], j["estadio"], j["id_clube_casa"], j["id_clube_fora"],
                f"{j['golos_casa']}-{j['golos_fora']}"
            ))

    def janela_novo_jogo(self):
        messagebox.showinfo("Info", "Janela de Jogo pronta para implementar")

    # ==================== FUNÇÕES AUXILIARES ====================
    def criar_treeview(self, parent, colunas):
        tree = ttk.Treeview(parent, columns=colunas, show="headings")
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill="both", expand=True, pady=10)
        return tree

    def adicionar_botoes(self, parent, atualizar_cmd, novo_cmd, remover_cmd=None):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
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

    def remover_item(self, tree, funcao_remover, atualizar):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um item!")
            return
        id_item = tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", f"Remover item ID {id_item}?"):
            funcao_remover(str(id_item))
            atualizar()

if __name__ == "__main__":
    root = tk.Tk()
    app = FootballManagerApp(root)
    root.mainloop()
