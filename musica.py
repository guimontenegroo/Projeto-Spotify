from typing import Any, Dict, List
from faixa_audio import FaixaAudio
from avaliacao import Avaliacao

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
