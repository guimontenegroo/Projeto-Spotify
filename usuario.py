from typing import Any, Dict, List, Optional
from playlist import Playlist
from musica import Musica

class Usuario:
    def __init__(self, id_usuario: int, nome: str):
        self.id_usuario: int = id_usuario
        self.nome = nome
        self._playlists: List[Playlist] = []

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = str(valor).strip()
        if not valor:
            raise ValueError("O nome do perfil nao pode ser vazio!")
        self.__nome = valor

    @property
    def playlists(self) -> List[Playlist]:
        return self._playlists

    def buscar_playlist(self, nome: str) -> Optional[Playlist]:
        return next((p for p in self._playlists if p.nome == nome), None)

    def criar_playlist(self, nome: str) -> Playlist:
        nome = nome.strip()
        if not nome:
            raise ValueError("O nome da playlist nao pode ser vazio!")
        if any(p.nome.lower() == nome.lower() for p in self._playlists):
            raise ValueError(f"Voce ja possui uma playlist chamada '{nome}'!")
        playlist = Playlist(nome)
        self._playlists.append(playlist)
        return playlist

    def renomear_playlist(self, playlist: Playlist, novo_nome: str) -> None:
        novo_nome = novo_nome.strip()
        if not novo_nome:
            raise ValueError("O nome da playlist nao pode ser vazio!")
        if any(p is not playlist and p.nome.lower() == novo_nome.lower() for p in self._playlists):
            raise ValueError(f"Voce ja possui uma playlist chamada '{novo_nome}'!")
        playlist.nome = novo_nome

    def remover_playlist(self, playlist: Playlist) -> None:
        if playlist not in self._playlists:
            raise ValueError("Essa playlist nao pertence a este perfil!")
        self._playlists.remove(playlist)

    def avaliar_musica(self, musica: Musica, nota: Any, comentario: str = "") -> None:
        musica.adicionar_avaliacao(nota, comentario)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "playlists": [p.to_dict() for p in self._playlists],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], catalogo: List[Musica]) -> "Usuario":
        usuario = cls(id_usuario=data["id_usuario"], nome=data["nome"])
        for p_data in data.get("playlists", []):
            usuario._playlists.append(Playlist.from_dict(p_data, catalogo))
        return usuario
