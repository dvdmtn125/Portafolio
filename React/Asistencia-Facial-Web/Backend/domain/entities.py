from dataclasses import dataclass, field
from datetime import datetime

import numpy as np


@dataclass(frozen=True)
class Persona:
    """Representa a alguien registrado en el sistema de asistencia."""
    id: str
    nombre: str
    encoding_facial: np.ndarray

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Persona):
            return NotImplemented
        return self.id == other.id


@dataclass(frozen=True)
class RegistroAsistencia:
    """Un evento de asistencia ya confirmado."""
    persona_id: str
    nombre: str
    momento: datetime
    confianza: float


@dataclass(frozen=True)
class ResultadoReconocimiento:
    """Salida cruda del reconocedor facial antes de decidir si se registra asistencia."""
    persona: Persona | None
    confianza: float
    reconocimiento: bool = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "reconocido", self.persona is not None)


@dataclass(frozen=True)
class ResultadoLiveness:
    """Resultado de analizar si una imagen corresponde a una persona real frente a la cámara,
    o a una foto/pantalla mostrando esa persona (spoofing)."""
    es_real: bool
    confianza: float