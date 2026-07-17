from pydantic import BaseModel


class FacturaCalcularRequest(BaseModel):
    cantidades: dict[str, list[float]]
    precios: dict[str, list[float]]