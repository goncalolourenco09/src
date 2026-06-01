import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label, Entry, Button, Frame

# Importações dos módulos
try:
    from clube import criar_clube, listar_clubes, remover_clube
    from jogador import criar_jogador, listar_jogadores, remover_jogador
    from treinador import criar_treinador, listar_treinadores, remover_treinador
    from jogo import criar_jogo, listar_jogos, remover_jogo
except ImportError as e:
    print(f"Aviso: Algum módulo não foi encontrado: {e}")


    def dummy(*args, **kwargs):
        return False, "Ficheiro .py em falta"


    if 'criar_clube' not in locals(): criar_clube = dummy
    if 'listar_clubes' not in locals(): listar_clubes = lambda: {}
    if 'remover_clube' not in locals(): remover_clube = dummy
    if 'criar_jogador' not in locals(): criar_jogador = dummy
    if 'listar_jogadores' not in locals(): listar_jogadores = lambda: {}
    if 'remover_jogador' not in locals(): remover_jogador = dummy
    if 'criar_treinador' not in locals(): criar_treinador = dummy
    if 'listar_treinadores' not in locals(): listar_treinadores = lambda: {}
    if 'remover_treinador' not in locals(): remover_treinador = dummy
    if 'criar_jogo' not in locals(): criar_jogo = dummy
    if 'listar_jogos' not in locals(): listar_jogos = lambda: {}
    if 'remover_jogo' not in locals(): remover_jogo = dummy


class FootballManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏆 Football Manager - Sistema de Gestão Profissional")
        self.root.geometry("1250x800")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar todas as abas (agora todas completas)
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
        win = Toplevel(self.root);
        win.title("Novo Clube");
        win.geometry("400x250");
        win.grab_set()
        f = Frame(win, padx=20, pady=20);
        f.pack()
        Label(f, text="Nome:").grid(row=0, column=0, sticky="w")
        e_nome = Entry(f, width=30);
        e_nome.grid(row=0, column=1, pady=5)
        Label(f, text="NIF:").grid(row=1, column=0, sticky="w")
        e_nif = Entry(f, width=30);
        e_nif.grid(row=1, column=1, pady=5)

        def salvar():
            n, ni = e_nome.get().strip(), e_nif.get().strip()
            if not n or not ni: return messagebox.showwarning("!", "Preencha tudo")
            s, m = criar_clube(n, ni)
            if s:
                win.destroy(); self.atualizar_clubes(); messagebox.showinfo("OK", "Clube criado!")
            else:
                messagebox.showerror("Erro", m)

        Button(f, text="Guardar", command=salvar, bg="green", fg="white", width=15).grid(row=2, columnspan=2, pady=20)

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
        for i in self.tree_jogadores.get_children(): self.tree_jogadores.delete(i)
        if not isinstance(jogadores, dict): return
        for id_j, j in jogadores.items():
            self.tree_jogadores.insert("", "end", values=(
                id_j, j.get("nome"), j.get("idade"), j.get("posicao", "").capitalize(),
                j.get("numero_camisa"), f"{float(j.get('salario', 0)):.2f}€"
            ))

    def janela_novo_jogador(self):
        win = Toplevel(self.root);
        win.title("Novo Jogador");
        win.geometry("450x550");
        win.grab_set()
        f = Frame(win, padx=20, pady=20);
        f.pack()
        lbls = ["Nome", "Data Nasc (AAAA-MM-DD)", "Camisola (1-99)", "Salário"]
        ents = []
        for i, c in enumerate(lbls):
            Label(f, text=c + ":").grid(row=i, column=0, sticky="w")
            e = Entry(f, width=30);
            e.grid(row=i, column=1, pady=8);
            ents.append(e)
        Label(f, text="Posição:").grid(row=4, column=0, sticky="w")
        cb = ttk.Combobox(f, values=["guarda-redes", "defesa", "médio", "avançado"], state="readonly", width=27)
        cb.grid(row=4, column=1, pady=8);
        cb.current(0)

        def salvar():
            v = [e.get().strip() for e in ents]
            if not all(v): return messagebox.showwarning("!", "Preencha tudo")
            s, m = criar_jogador(v[0], v[1], v[2], cb.get(), v[3])
            if s:
                win.destroy(); self.atualizar_jogadores(); messagebox.showinfo("OK", "Jogador criado!")
            else:
                messagebox.showerror("Erro", m)

        Button(f, text="💾 Guardar", command=salvar, bg="green", fg="white", width=20).grid(row=5, columnspan=2, pady=20)

    def remover_jogador(self):
        self.remover_item(self.tree_jogadores, remover_jogador, self.atualizar_jogadores)

    # ====================== TREINADORES ======================
    def criar_aba_treinadores(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Treinadores")
        self.tree_treinadores = self.criar_treeview(frame, ["ID", "Nome", "Nacionalidade", "Licença", "ID Clube"])
        self.adicionar_botoes(frame, self.atualizar_treinadores, self.janela_novo_treinador, self.remover_treinador)
        self.atualizar_treinadores()

    def atualizar_treinadores(self):
        self.atualizar_tree(self.tree_treinadores, listar_treinadores(),
                            ["nome", "nacionalidade", "licenca_UEFA", "id_clube"])

    def janela_novo_treinador(self):
        win = Toplevel(self.root);
        win.title("Novo Treinador");
        win.geometry("450x450");
        win.grab_set()
        f = Frame(win, padx=20, pady=20);
        f.pack()
        lbls = ["Nome", "Nacionalidade", "Data Nasc (AAAA-MM-DD)", "Licença (A/B/PRO)"]
        ents = []
        for i, c in enumerate(lbls):
            Label(f, text=c + ":").grid(row=i, column=0, sticky="w")
            e = Entry(f, width=30);
            e.grid(row=i, column=1, pady=8);
            ents.append(e)

        def salvar():
            v = [e.get().strip() for e in ents]
            if not all(v): return messagebox.showwarning("!", "Preencha tudo")
            s, m = criar_treinador(v[0], v[1], v[2], v[3])
            if s:
                win.destroy(); self.atualizar_treinadores(); messagebox.showinfo("OK", "Treinador criado!")
            else:
                messagebox.showerror("Erro", m)

        Button(f, text="💾 Guardar", command=salvar, bg="green", fg="white", width=20).grid(row=4, columnspan=2, pady=20)

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
        for i in self.tree_jogos.get_children(): self.tree_jogos.delete(i)
        if not isinstance(jogos, dict): return
        for id_j, j in jogos.items():
            self.tree_jogos.insert("", "end", values=(
                id_j, j.get("data"), j.get("estadio"), j.get("id_clube_casa"), j.get("id_clube_fora"),
                f"{j.get('golos_casa', 0)}-{j.get('golos_fora', 0)}"
            ))

    def janela_novo_jogo(self):
        win = Toplevel(self.root);
        win.title("Novo Jogo");
        win.geometry("450x550");
        win.grab_set()
        f = Frame(win, padx=20, pady=20);
        f.pack()
        lbls = ["Data (AAAA-MM-DD)", "Estádio", "ID Clube Casa", "ID Clube Fora", "Golos Casa", "Golos Fora"]
        ents = []
        for i, l in enumerate(lbls):
            Label(f, text=l + ":").grid(row=i, column=0, sticky="w")
            e = Entry(f, width=30);
            e.grid(row=i, column=1, pady=5);
            ents.append(e)

        def salvar():
            v = [e.get().strip() for e in ents]
            if not all(v): return messagebox.showwarning("!", "Preencha tudo")
            try:
                s, m = criar_jogo(v[0], v[1], int(v[2]), int(v[3]), int(v[4]), int(v[5]))
                if s:
                    win.destroy(); self.atualizar_jogos(); messagebox.showinfo("OK", "Jogo registado!")
                else:
                    messagebox.showerror("Erro", m)
            except ValueError:
                messagebox.showerror("Erro", "IDs e Golos devem ser números")

        Button(f, text="💾 Guardar Jogo", command=salvar, bg="green", fg="white", width=20).grid(row=6, columnspan=2,
                                                                                                pady=20)

    def remover_jogo(self):
        self.remover_item(self.tree_jogos, remover_jogo, self.atualizar_jogos)

    # ====================== AUXILIARES ======================
    def criar_treeview(self, parent, colunas):
        f = Frame(parent);
        f.pack(fill="both", expand=True, pady=10)
        t = ttk.Treeview(f, columns=colunas, show="headings")
        for c in colunas: t.heading(c, text=c); t.column(c, width=120, anchor="center")
        t.pack(fill="both", expand=True);
        return t

    def adicionar_botoes(self, parent, att, novo, rem):
        f = Frame(parent);
        f.pack(fill="x", pady=5)
        Button(f, text="🔄 Atualizar", command=att).pack(side="left", padx=5)
        Button(f, text="➕ Novo", command=novo).pack(side="left", padx=5)
        Button(f, text="🗑 Remover", command=rem).pack(side="left", padx=5)

    def atualizar_tree(self, tree, dados, campos):
        for i in tree.get_children(): tree.delete(i)
        if not isinstance(dados, dict): return
        for id_i, item in dados.items():
            tree.insert("", "end", values=[id_i] + [item.get(c, "N/A") for c in campos])

    def remover_item(self, tree, func, att):
        sel = tree.selection()
        if not sel: return messagebox.showwarning("!", "Selecione um item")
        id_i = tree.item(sel[0])["values"][0]
        if messagebox.askyesno("?", f"Remover ID {id_i}?"):
            s, m = func(str(id_i))
            if s:
                att(); messagebox.showinfo("OK", m)
            else:
                messagebox.showerror("Erro", m)


if __name__ == "__main__":
    root = tk.Tk()
    app = FootballManagerApp(root)
    root.mainloop()
