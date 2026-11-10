import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from avaliacao import Avaliacao
from servicos import criar_usuario, renomear_usuario

class Playlists:
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

