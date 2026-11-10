from typing import Any, Dict

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
