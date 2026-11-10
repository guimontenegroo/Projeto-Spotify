from typing import Any, Dict
from faixa_audio import FaixaAudio

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
