import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from projeto import (
    ARQUIVO_PADRAO,
    Avaliacao,
    carregar_dados,
    catalogo_padrao,
    criar_usuario,
    propagandas_padrao,
    renomear_usuario,
    salvar_dados,
)


class SpotifyDark(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spotify POO - Dark Edition")
        self.geometry("760x560")
        self.minsize(680, 500)

        self.BG_DARK = "#121212"
        self.BG_CARD = "#1E1E1E"
        self.BG_ITEM = "#282828"
        self.ACCENT_GREEN = "#1DB954"
        self.TEXT_WHITE = "#FFFFFF"
        self.TEXT_MUTED = "#B3B3B3"
        self.configure(bg=self.BG_DARK)

        self.propagandas = propagandas_padrao()
        self.usuarios, self.catalogo, self.user_atual = carregar_dados(
            ARQUIVO_PADRAO, catalogo_padrao()
        )

        self._aplicar_estilos()
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self._mostrar_tela_selecao_perfil()

    def _aplicar_estilos(self):
        s = self.style = ttk.Style()
        s.theme_use("clam")
        s.configure(".", background=self.BG_DARK, foreground=self.TEXT_WHITE, font=("Segoe UI", 10))

        s.configure("TFrame", background=self.BG_DARK)
        s.configure("Card.TFrame", background=self.BG_CARD)

        s.configure("TLabel", background=self.BG_DARK, foreground=self.TEXT_WHITE)
        s.configure("Card.TLabel", background=self.BG_CARD, foreground=self.TEXT_WHITE)
        s.configure("Muted.TLabel", foreground=self.TEXT_MUTED)
        s.configure("CardMuted.TLabel", background=self.BG_CARD, foreground=self.TEXT_MUTED)
        s.configure("Header.TLabel", background=self.BG_CARD, font=("Segoe UI", 16, "bold"))

        s.configure("TButton", background=self.BG_ITEM, foreground=self.TEXT_WHITE,
                    borderwidth=0, focuscolor="none", padding=6)
        s.map("TButton", background=[("active", "#383838")])
        s.configure("Green.TButton", background=self.ACCENT_GREEN, foreground="#000000",
                    font=("Segoe UI", 10, "bold"), padding=8)
        s.map("Green.TButton", background=[("active", "#1ed760")])
        s.configure("ProfileCard.TButton", background=self.BG_ITEM, foreground=self.TEXT_WHITE,
                    font=("Segoe UI", 11, "bold"), padding=12)
        s.map("ProfileCard.TButton", background=[("active", "#383838")])

        s.configure("TNotebook", background=self.BG_DARK, borderwidth=0)
        s.configure("TNotebook.Tab", background=self.BG_CARD, foreground=self.TEXT_MUTED,
                    padding=[16, 8], font=("Segoe UI", 10, "bold"))
        s.map("TNotebook.Tab", background=[("selected", self.BG_DARK)],
              foreground=[("selected", self.ACCENT_GREEN)])

        s.configure("Treeview", background=self.BG_CARD, foreground=self.TEXT_WHITE,
                    fieldbackground=self.BG_CARD, rowheight=28, borderwidth=0)
        s.configure("Treeview.Heading", background=self.BG_ITEM, foreground=self.ACCENT_GREEN,
                    font=("Segoe UI", 10, "bold"), borderwidth=0)
        s.map("Treeview", background=[("selected", "#333333")],
              foreground=[("selected", self.ACCENT_GREEN)])

        s.configure("TCombobox", background=self.BG_ITEM, foreground=self.TEXT_WHITE,
                    fieldbackground=self.BG_ITEM, arrowcolor=self.ACCENT_GREEN)

    def _limpar_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def _salvar(self):
        id_atual = self.user_atual.id_usuario if self.user_atual else None
        if not salvar_dados(self.usuarios, self.catalogo, id_atual):
            messagebox.showerror("Erro", "Nao foi possivel salvar os dados no disco.")

    def _musica_selecionada(self, aviso):
        sel = self.tree_musicas.selection()
        if not sel:
            messagebox.showwarning("Aviso", aviso)
            return None
        return self.catalogo[int(sel[0])]

    def _playlist_atual(self):
        return self.user_atual.buscar_playlist(self.combo_playlists.get())

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

    def _mostrar_tela_principal(self):
        self._limpar_container()

        top_bar = ttk.Frame(self.container, style="Card.TFrame", padding=10)
        top_bar.pack(fill="x", padx=12, pady=(12, 6))
        ttk.Label(top_bar, text=f"Perfil Ativo: {self.user_atual.nome}", style="Card.TLabel",
                  font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
        ttk.Button(top_bar, text="Trocar Perfil", style="Green.TButton",
                   command=self._mostrar_tela_selecao_perfil).pack(side="right", padx=5)

        self.lbl_status = ttk.Label(self.container, text=f"Bem-vindo, {self.user_atual.nome}!",
                                    style="Muted.TLabel", padding=6)
        self.lbl_status.pack(fill="x", side="bottom", padx=12)

        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=6)

        self.aba_catalogo = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.aba_catalogo, text="Catalogo de Musicas")
        self._construir_aba_catalogo()

        self.aba_playlists = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.aba_playlists, text="Playlists")
        self._construir_aba_playlists()

        self._atualizar_catalogo()
        self._atualizar_playlists()

    def _construir_aba_catalogo(self):
        colunas = ("titulo", "artista", "genero", "duracao", "media")
        self.tree_musicas = ttk.Treeview(self.aba_catalogo, columns=colunas,
                                         show="headings", selectmode="browse")
        for col, texto, larg, anc in [
            ("titulo", "Titulo", 180, "w"), ("artista", "Artista", 140, "w"),
            ("genero", "Genero", 110, "w"), ("duracao", "Duracao", 80, "center"),
            ("media", "Media", 70, "center"),
        ]:
            self.tree_musicas.heading(col, text=texto)
            self.tree_musicas.column(col, width=larg, anchor=anc)
        self.tree_musicas.pack(fill="both", expand=True, pady=(0, 10))

        btn_box = ttk.Frame(self.aba_catalogo)
        btn_box.pack(fill="x")
        ttk.Button(btn_box, text="Reproduzir", style="Green.TButton",
                   command=self._tocar_musica).pack(side="left", padx=5)
        ttk.Button(btn_box, text="Avaliar Musica", command=self._avaliar_musica).pack(side="left", padx=5)
        ttk.Button(btn_box, text="Ver Avaliacoes", command=self._ver_avaliacoes).pack(side="left", padx=5)

    def _construir_aba_playlists(self):
        topo = ttk.Frame(self.aba_playlists)
        topo.pack(fill="x", pady=(0, 10))

        ttk.Label(topo, text="Playlist:").pack(side="left", padx=(0, 5))
        self.combo_playlists = ttk.Combobox(topo, state="readonly", width=25)
        self.combo_playlists.pack(side="left", padx=5)
        self.combo_playlists.bind("<<ComboboxSelected>>", self._carregar_faixas_playlist)

        ttk.Button(topo, text="+ Criar", style="Green.TButton", command=self._criar_playlist).pack(side="left", padx=5)
        ttk.Button(topo, text="Excluir", command=self._excluir_playlist).pack(side="left", padx=5)
        ttk.Button(topo, text="Tocar Tudo", style="Green.TButton", command=self._tocar_playlist).pack(side="right", padx=5)

        colunas = ("titulo", "artista", "duracao")
        self.tree_playlist = ttk.Treeview(self.aba_playlists, columns=colunas,
                                          show="headings", selectmode="browse")
        for col, texto, larg, anc in [
            ("titulo", "Titulo", 240, "w"), ("artista", "Artista", 180, "w"),
            ("duracao", "Duracao", 100, "center"),
        ]:
            self.tree_playlist.heading(col, text=texto)
            self.tree_playlist.column(col, width=larg, anchor=anc)
        self.tree_playlist.pack(fill="both", expand=True, pady=(0, 10))

        btn_box = ttk.Frame(self.aba_playlists)
        btn_box.pack(fill="x")
        ttk.Button(btn_box, text="+ Adicionar Musica", command=self._adicionar_musica_playlist).pack(side="left", padx=5)
        ttk.Button(btn_box, text="- Remover Musica", command=self._remover_musica_playlist).pack(side="left", padx=5)

    def _atualizar_catalogo(self):
        self.tree_musicas.delete(*self.tree_musicas.get_children())
        for i, m in enumerate(self.catalogo):
            media = f"{m.media_notas:.1f}" if m.media_notas > 0 else "-"
            self.tree_musicas.insert("", "end", iid=str(i),
                                     values=(m.titulo, m.artista, m.genero, m.duracao_formatada, media))

    def _atualizar_playlists(self):
        nomes = [p.nome for p in self.user_atual.playlists]
        self.combo_playlists["values"] = nomes
        self.combo_playlists.set(nomes[0] if nomes else "")
        self._carregar_faixas_playlist()

    def _carregar_faixas_playlist(self, event=None):
        self.tree_playlist.delete(*self.tree_playlist.get_children())
        pl = self._playlist_atual()
        if pl:
            for i, f in enumerate(pl.faixas):
                self.tree_playlist.insert("", "end", iid=str(i),
                                          values=(f.titulo, getattr(f, "artista", "N/A"), f.duracao_formatada))

    def _tocar_musica(self):
        musica = self._musica_selecionada("Selecione uma musica do catalogo para tocar.")
        if not musica:
            return
        try:
            msg = musica.reproduzir()
        except RuntimeError as e:
            messagebox.showerror("Erro", str(e))
            return
        musica.parar()
        self.lbl_status.config(text=msg)
        messagebox.showinfo("Reproduzindo", msg)

    def _avaliar_musica(self):
        musica = self._musica_selecionada("Selecione uma musica do catalogo para avaliar.")
        if not musica:
            return
        nota = simpledialog.askstring("Avaliar Musica", f"Nota de 1 a 5 para '{musica.titulo}':", parent=self)
        if nota is None:
            return
        try:
            Avaliacao.validar_nota(nota)
            comentario = simpledialog.askstring("Comentario", "Deixe um comentario (opcional):", parent=self) or ""
            self.user_atual.avaliar_musica(musica, nota, comentario)
        except ValueError as e:
            messagebox.showerror("Erro de Validacao", str(e))
            return
        self._salvar()
        self._atualizar_catalogo()
        messagebox.showinfo("Sucesso", "Avaliacao registrada com sucesso!")

    def _ver_avaliacoes(self):
        musica = self._musica_selecionada("Selecione uma musica para ver as avaliacoes.")
        if not musica:
            return
        if not musica.avaliacoes:
            messagebox.showinfo("Avaliacoes", f"'{musica.titulo}' ainda nao possui avaliacoes.")
            return
        linhas = [f"Avaliacoes de '{musica.titulo}' (Media: {musica.media_notas:.1f}):\n"]
        for a in musica.avaliacoes:
            linhas.append(f"- Nota {a.nota:g}: {a.comentario or '(Sem comentario)'}")
        messagebox.showinfo("Avaliacoes", "\n".join(linhas))

    def _criar_playlist(self):
        nome = simpledialog.askstring("Criar Playlist", "Nome da playlist:", parent=self)
        if nome is None:
            return
        try:
            pl = self.user_atual.criar_playlist(nome)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        self._salvar()
        self._atualizar_playlists()
        self.combo_playlists.set(pl.nome)
        self._carregar_faixas_playlist()

    def _excluir_playlist(self):
        pl = self._playlist_atual()
        if not pl:
            return
        if messagebox.askyesno("Confirmar", f"Excluir a playlist '{pl.nome}'?"):
            try:
                self.user_atual.remover_playlist(pl)
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
                return
            self._salvar()
            self._atualizar_playlists()

    def _adicionar_musica_playlist(self):
        pl = self._playlist_atual()
        if not pl:
            messagebox.showwarning("Aviso", "Crie ou selecione uma playlist primeiro.")
            return
        musica = self._musica_selecionada("Selecione uma musica na aba 'Catalogo de Musicas' para adicionar.")
        if not musica:
            return
        try:
            pl.adicionar_faixa(musica)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        self._salvar()
        self._carregar_faixas_playlist()
        messagebox.showinfo("Sucesso", f"'{musica.titulo}' adicionada a playlist '{pl.nome}'!")

    def _remover_musica_playlist(self):
        pl = self._playlist_atual()
        sel = self.tree_playlist.selection()
        if not pl or not sel:
            messagebox.showwarning("Aviso", "Selecione uma musica dentro da playlist para remover.")
            return
        try:
            pl.remover_faixa(pl.faixas[int(sel[0])])
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return
        self._salvar()
        self._carregar_faixas_playlist()

    def _tocar_playlist(self):
        pl = self._playlist_atual()
        if not pl:
            return
        try:
            log = pl.reproduzir(self.propagandas)
        except ValueError as e:
            messagebox.showinfo("Playlist Vazia", str(e))
        except RuntimeError as e:
            messagebox.showerror("Erro", str(e))
        else:
            cabecalho = f"--- Reproduzindo Playlist: {pl.nome} ---"
            messagebox.showinfo("Tocando Playlist", "\n".join([cabecalho] + log))


if __name__ == "__main__":
    SpotifyDark().mainloop()
