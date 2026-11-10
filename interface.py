import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from catalogo import catalogo_padrao, propagandas_padrao
from servicos import ARQUIVO_PADRAO, carregar_dados, salvar_dados
from interface_perfis import Perfis
from interface_catalogo import Catalogo
from interface_playlists import Playlists

class SpotifyDark(Perfis, Catalogo, Playlists, tk.Tk):
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


if __name__ == "__main__":
    SpotifyDark().mainloop()
