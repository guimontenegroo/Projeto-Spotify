import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from avaliacao import Avaliacao
from servicos import criar_usuario, renomear_usuario

class Perfis:
    def _mostrar_tela_selecao_perfil(self):
        self._limpar_container()

        card = ttk.Frame(self.container, style="Card.TFrame", padding=30)
        card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=440)

        ttk.Label(card, text="Quem esta ouvindo?", style="Header.TLabel").pack(pady=(0, 5))
        ttk.Label(card, text="Selecione um perfil abaixo ou crie um novo para acessar",
                  style="CardMuted.TLabel").pack(pady=(0, 20))

        frame_perfis = ttk.Frame(card, style="Card.TFrame")
        frame_perfis.pack(fill="both", expand=True, pady=5)

        if not self.usuarios:
            ttk.Label(frame_perfis, text="Nenhum perfil cadastrado ainda.",
                      style="CardMuted.TLabel").pack(pady=20)
        for user in self.usuarios:
            ttk.Button(frame_perfis, text=user.nome, style="ProfileCard.TButton",
                       command=lambda u=user: self._entrar_com_perfil(u)).pack(fill="x", pady=4)

        btn_box = ttk.Frame(card, style="Card.TFrame")
        btn_box.pack(fill="x", pady=(15, 0))
        ttk.Button(btn_box, text="+ Criar Novo Perfil", style="Green.TButton",
                   command=self._novo_perfil).pack(side="left", fill="x", expand=True, padx=4)
        if self.usuarios:
            ttk.Button(btn_box, text="Gerenciar Perfis",
                       command=self._gerenciar_perfis).pack(side="right", padx=4)

    def _entrar_com_perfil(self, usuario):
        self.user_atual = usuario
        self._salvar()
        self._mostrar_tela_principal()

    def _novo_perfil(self):
        nome = simpledialog.askstring("Novo Perfil", "Digite o nome do novo perfil:", parent=self)
        if nome is None:
            return
        try:
            novo = criar_usuario(self.usuarios, nome)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        self._entrar_com_perfil(novo)

    def _gerenciar_perfis(self):
        janela = tk.Toplevel(self)
        janela.title("Gerenciar Perfis")
        janela.geometry("380x300")
        janela.configure(bg=self.BG_CARD)

        ttk.Label(janela, text="Opcoes de Perfis", style="Card.TLabel",
                  font=("Segoe UI", 12, "bold")).pack(pady=10)

        lista = tk.Listbox(janela, bg=self.BG_ITEM, fg=self.TEXT_WHITE, borderwidth=0,
                           selectbackground=self.ACCENT_GREEN, selectforeground="#000000")
        lista.pack(fill="both", expand=True, padx=15, pady=5)
        for u in self.usuarios:
            lista.insert("end", u.nome)

        def renomear():
            sel = lista.curselection()
            if not sel:
                return
            user = self.usuarios[sel[0]]
            novo_nome = simpledialog.askstring("Renomear", f"Novo nome para '{user.nome}':",
                                               initialvalue=user.nome, parent=janela)
            if novo_nome is None:
                return
            try:
                renomear_usuario(self.usuarios, user, novo_nome)
            except ValueError as e:
                messagebox.showerror("Erro", str(e), parent=janela)
                return
            self._salvar()
            janela.destroy()
            self._mostrar_tela_selecao_perfil()

        def excluir():
            sel = lista.curselection()
            if not sel:
                return
            user = self.usuarios[sel[0]]
            if messagebox.askyesno("Confirmar",
                                   f"Excluir o perfil '{user.nome}' e todas as suas playlists?",
                                   parent=janela):
                self.usuarios.remove(user)
                if self.user_atual is user:
                    self.user_atual = None
                self._salvar()
                janela.destroy()
                self._mostrar_tela_selecao_perfil()

        botoes = ttk.Frame(janela, style="Card.TFrame")
        botoes.pack(fill="x", padx=15, pady=10)
        ttk.Button(botoes, text="Renomear", command=renomear).pack(side="left", padx=5)
        ttk.Button(botoes, text="Excluir", command=excluir).pack(side="right", padx=5)

