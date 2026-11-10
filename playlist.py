from typing import Any, Dict, List, Optional
from faixa_audio import FaixaAudio
from musica import Musica
from propaganda import Propaganda

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
