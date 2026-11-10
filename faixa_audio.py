from typing import Any, Dict

def formatar_duracao(segundos: int) -> str:
    segundos = max(0, int(segundos))
    horas, resto = divmod(segundos, 3600)
    minutos, seg = divmod(resto, 60)
    if horas:
        return f"{horas}:{minutos:02d}:{seg:02d}"
    return f"{minutos}:{seg:02d}"

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
