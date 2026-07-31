from datetime import date

import numpy as np

from domain.entities import Persona, RegistroAsistencia, ResultadoReconocimiento
from domain.ports import (
    ReconocedorFacialPort,
    RepositorioAsistenciaPort,
    RepositorioPersonasPort,
)


class FakeReconocedorFacial(ReconocedorFacialPort):
    """
    Doble de prueba controlable: en vez de procesar imágenes reales,
    devuelve lo que el test configure de antemano.
    """

    def __init__(self):
        self.encoding_a_devolver: np.ndarray | None = np.random.rand(128)
        self.resultado_a_devolver: ResultadoReconocimiento = ResultadoReconocimiento(
            persona=None, confianza=0.0
        )
        self.imagenes_recibidas: list[bytes] = []

    def calcular_encoding(self, imagen_bytes: bytes) -> np.ndarray | None:
        self.imagenes_recibidas.append(imagen_bytes)
        return self.encoding_a_devolver

    def reconocer(
        self, imagen_bytes: bytes, personas_conocidas: list[Persona]
    ) -> ResultadoReconocimiento:
        self.imagenes_recibidas.append(imagen_bytes)
        return self.resultado_a_devolver


class FakeRepositorioPersonas(RepositorioPersonasPort):
    def __init__(self):
        self._personas: dict[str, Persona] = {}

    def guardar(self, persona: Persona) -> None:
        self._personas[persona.id] = persona

    def listar_todas(self) -> list[Persona]:
        return list(self._personas.values())

    def buscar_por_id(self, persona_id: str) -> Persona | None:
        return self._personas.get(persona_id)


class FakeRepositorioAsistencia(RepositorioAsistenciaPort):
    def __init__(self):
        self._registros: list[RegistroAsistencia] = []
        self._ids_ya_regitrados_hoy: set[str] = set()

    def registrar(self, registro: RegistroAsistencia) -> None:
        self._registros.append(registro)
        self._ids_ya_regitrados_hoy.add(registro.persona_id)

    def ya_registrado_hoy(self, persona_id: str):
        return persona_id in self._ids_ya_regitrados_hoy

    def listar_por_fecha(self, fecha: date) -> list[RegistroAsistencia]:
        return [r for r in self._registros if r.momento.date() == fecha]