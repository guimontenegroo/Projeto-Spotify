import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from avaliacao import Avaliacao
from servicos import criar_usuario, renomear_usuario

class Catalogo:
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

    def _atualizar_catalogo(self):
        self.tree_musicas.delete(*self.tree_musicas.get_children())
        for i, m in enumerate(self.catalogo):
            media = f"{m.media_notas:.1f}" if m.media_notas > 0 else "-"
            self.tree_musicas.insert("", "end", iid=str(i),
                                     values=(m.titulo, m.artista, m.genero, m.duracao_formatada, media))

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

