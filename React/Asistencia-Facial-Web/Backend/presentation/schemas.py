from datetime import datetime

from pydantic import BaseModel


class PersonaEntrada(BaseModel):
    id: str
    nombre: str


class PersonaSalida(BaseModel):
    id: str
    nombre: str


class ReconocimientoSalida(BaseModel):
    reconocido: bool
    persona_id: str | None
    nombre: str | None
    confianza: float


class RegistroAsistenciaSalida(BaseModel):
    persona_id: str
    nombre: str
    momento: datetime
    confianza: float