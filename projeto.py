import json
import os
import shutil
from typing import Any, Dict, List, Optional, Tuple

ARQUIVO_PADRAO = "dados.json"


def formatar_duracao(segundos: int) -> str:
    segundos = max(0, int(segundos))
    horas, resto = divmod(segundos, 3600)
    minutos, seg = divmod(resto, 60)
    if horas:
        return f"{horas}:{minutos:02d}:{seg:02d}"
    return f"{minutos}:{seg:02d}"


class Avaliacao:
    def __init__(self, nota: Any, comentario: str = ""):
        self.nota = nota
        self.comentario: str = str(comentario).strip()

    @staticmethod
    def validar_nota(valor: Any) -> float:
        if isinstance(valor, str):
            valor = valor.strip().replace(",", ".")
        try:
            nota = float(valor)
        except (ValueError, TypeError):
            raise ValueError("A nota deve ser um numero valido!") from None
        if not (1.0 <= nota <= 5.0):
            raise ValueError("A nota deve estar entre 1 e 5!")
        return nota

    @property
    def nota(self) -> float:
        return self.__nota

    @nota.setter
    def nota(self, valor: Any) -> None:
        self.__nota = self.validar_nota(valor)

    def to_dict(self) -> Dict[str, Any]:
        return {"nota": self.nota, "comentario": self.comentario}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Avaliacao":
        return cls(nota=data["nota"], comentario=data.get("comentario", ""))


class FaixaAudio:
    def __init__(self, titulo: str, duracao_segundos: int):
        self.titulo: str = titulo
        self.duracao_segundos: int = duracao_segundos
        self.esta_tocando: bool = False

    @property
    def duracao_formatada(self) -> str:
        return formatar_duracao(self.duracao_segundos)

    def reproduzir(self) -> str:
        if self.esta_tocando:
            raise RuntimeError(f"A faixa '{self.titulo}' ja esta sendo reproduzida!")
        self.esta_tocando = True
        return f"Tocando: {self.titulo} ({self.duracao_formatada})"

    def parar(self) -> None:
        self.esta_tocando = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": "FaixaAudio",
            "titulo": self.titulo,
            "duracao_segundos": self.duracao_segundos,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FaixaAudio":
        return cls(titulo=data["titulo"], duracao_segundos=data["duracao_segundos"])


class Musica(FaixaAudio):
    def __init__(self, titulo: str, artista: str, genero: str, duracao_segundos: int):
        super().__init__(titulo, duracao_segundos)
        self.artista: str = artista
        self.genero: str = genero
        self._avaliacoes: List[Avaliacao] = []

    @property
    def avaliacoes(self) -> List[Avaliacao]:
        return self._avaliacoes

    @property
    def media_notas(self) -> float:
        if not self._avaliacoes:
            return 0.0
        return round(sum(a.nota for a in self._avaliacoes) / len(self._avaliacoes), 1)

    def adicionar_avaliacao(self, nota: Any, comentario: str = "") -> None:
        self._avaliacoes.append(Avaliacao(nota, comentario))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": "Musica",
            "titulo": self.titulo,
            "artista": self.artista,
            "genero": self.genero,
            "duracao_segundos": self.duracao_segundos,
            "avaliacoes": [a.to_dict() for a in self._avaliacoes],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Musica":
        musica = cls(
            titulo=data["titulo"],
            artista=data["artista"],
            genero=data["genero"],
            duracao_segundos=data["duracao_segundos"],
        )
        for a_data in data.get("avaliacoes", []):
            musica._avaliacoes.append(Avaliacao.from_dict(a_data))
        return musica


class Propaganda(FaixaAudio):
    def __init__(self, titulo: str, anunciante: str, duracao_segundos: int):
        super().__init__(titulo, duracao_segundos)
        self.anunciante: str = anunciante

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": "Propaganda",
            "titulo": self.titulo,
            "anunciante": self.anunciante,
            "duracao_segundos": self.duracao_segundos,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Propaganda":
        return cls(
            titulo=data["titulo"],
            anunciante=data["anunciante"],
            duracao_segundos=data["duracao_segundos"],
        )


class Playlist:
    def __init__(self, nome: str):
        self.nome: str = nome
        self.esta_tocando: bool = False
        self._faixas: List[FaixaAudio] = []

    @property
    def faixas(self) -> List[FaixaAudio]:
        return self._faixas

    @property
    def duracao_total(self) -> int:
        return sum(f.duracao_segundos for f in self._faixas)

    def adicionar_faixa(self, faixa: FaixaAudio) -> None:
        if any(f.titulo.lower() == faixa.titulo.lower() for f in self._faixas):
            raise ValueError(f"A musica '{faixa.titulo}' ja esta na playlist '{self.nome}'!")
        self._faixas.append(faixa)

    def remover_faixa(self, faixa: FaixaAudio) -> None:
        if faixa not in self._faixas:
            raise ValueError(f"A musica '{faixa.titulo}' nao esta na playlist '{self.nome}'!")
        self._faixas.remove(faixa)

    def reproduzir(self, propagandas: Optional[List[Propaganda]] = None) -> List[str]:
        if self.esta_tocando:
            raise RuntimeError(f"A playlist '{self.nome}' ja esta sendo reproduzida!")
        if not self._faixas:
            raise ValueError(f"A playlist '{self.nome}' esta vazia!")

        self.esta_tocando = True
        log: List[str] = []
        try:
            proxima_prop = 0
            for i, faixa in enumerate(self._faixas, 1):
                log.append(self._tocar(faixa))

                if propagandas and i % 2 == 0 and i < len(self._faixas):
                    log.append(self._tocar(propagandas[proxima_prop % len(propagandas)]))
                    proxima_prop += 1
        finally:
            self.esta_tocando = False
        return log

    @staticmethod
    def _tocar(faixa: FaixaAudio) -> str:
        msg = faixa.reproduzir()
        faixa.parar()
        return msg

    def to_dict(self) -> Dict[str, Any]:
        return {"nome": self.nome, "faixas_titulos": [f.titulo for f in self._faixas]}

    @classmethod
    def from_dict(cls, data: Dict[str, Any], catalogo: List[Musica]) -> "Playlist":
        playlist = cls(nome=data["nome"])
        mapa_catalogo = {m.titulo.lower(): m for m in catalogo}
        for titulo in data.get("faixas_titulos", []):
            musica = mapa_catalogo.get(titulo.lower())
            if musica is not None:
                playlist._faixas.append(musica)
        return playlist


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


def criar_usuario(usuarios: List[Usuario], nome: str) -> Usuario:
    nome = nome.strip()
    if any(u.nome.lower() == nome.lower() for u in usuarios):
        raise ValueError(f"Ja existe um perfil chamado '{nome}'.")
    novo_id = max((u.id_usuario for u in usuarios), default=0) + 1
    usuario = Usuario(novo_id, nome)
    usuarios.append(usuario)
    return usuario


def renomear_usuario(usuarios: List[Usuario], usuario: Usuario, novo_nome: str) -> None:
    novo_nome = novo_nome.strip()
    if any(u is not usuario and u.nome.lower() == novo_nome.lower() for u in usuarios):
        raise ValueError(f"Ja existe um perfil chamado '{novo_nome}'.")
    usuario.nome = novo_nome


def catalogo_padrao() -> List[Musica]:
    return [
        Musica("Let Down", "Radiohead", "Alternative Rock", 299),
        Musica("Like a Stone", "Audioslave", "Hard Rock", 294),
        Musica("Hino do Santos", "Santos Futebol Clube", "Hino", 180),
        Musica("Tema do GTA 6", "Rockstar Games", "Trilha Sonora", 210),
        Musica("Billie Jean", "Michael Jackson", "Pop", 294),
        Musica("Largado as Tracas", "Ze Neto & Cristiano", "Sertanejo", 197),
    ]


def propagandas_padrao() -> List[Propaganda]:
    return [
        Propaganda("Assine o Premium e ouca sem anuncios", "Spotify POO", 15),
        Propaganda("Oferta de fim de semana", "Mercado Central", 20),
        Propaganda("Peca ja a sua pizza", "Pizzaria do Ze", 12),
    ]


def salvar_dados(
    usuarios: List[Usuario],
    catalogo: List[Musica],
    id_usuario_atual: Optional[int] = None,
    arquivo: str = ARQUIVO_PADRAO,
) -> bool:
    dados = {
        "id_usuario_atual": id_usuario_atual,
        "usuarios": [u.to_dict() for u in usuarios],
        "catalogo": [m.to_dict() for m in catalogo],
    }
    temporario = arquivo + ".tmp"
    try:
        with open(temporario, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        os.replace(temporario, arquivo)
        return True
    except OSError:
        return False


def mesclar_catalogo(
    catalogo: List[Musica], catalogo_base: Optional[List[Musica]]
) -> List[Musica]:
    if not catalogo_base:
        return catalogo
    existentes = {m.titulo.lower() for m in catalogo}
    catalogo.extend(m for m in catalogo_base if m.titulo.lower() not in existentes)
    return catalogo


def carregar_dados(
    arquivo: str = ARQUIVO_PADRAO,
    catalogo_base: Optional[List[Musica]] = None,
) -> Tuple[List[Usuario], List[Musica], Optional[Usuario]]:
    catalogo_base = catalogo_base or []
    if not os.path.exists(arquivo):
        return [], catalogo_base, None

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        catalogo = [Musica.from_dict(m) for m in dados.get("catalogo", [])]
        catalogo = mesclar_catalogo(catalogo, catalogo_base)
        usuarios = [Usuario.from_dict(u, catalogo) for u in dados.get("usuarios", [])]

        id_atual = dados.get("id_usuario_atual")
        usuario_atual = next((u for u in usuarios if u.id_usuario == id_atual), None)
        if usuario_atual is None and usuarios:
            usuario_atual = usuarios[0]
        return usuarios, catalogo, usuario_atual
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        try:
            shutil.copy(arquivo, arquivo + ".corrompido")
        except OSError:
            pass
        return [], catalogo_base, None
