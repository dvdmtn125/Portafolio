from pydantic import BaseModel


class ReciboGenerarRequest(BaseModel):
    items: dict[str, list[tuple[str, float, float]]]
    calculo: dict[str, float]
    numero_recibo: str | None = None


class RecibogenerarRespuesta(BaseModel):
    recibo: str