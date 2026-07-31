from datetime import datetime

from domain.entities import RegistroAsistencia, ResultadoReconocimiento
from domain.ports import (
    ReconocedorFacialPort,
    RepositorioAsistenciaPort,
    RepositorioPersonasPort,
)


class ReconocerYMarcarAsistencia:
    """
    Caso de uso principal del flujo de webcam en vivo:
    recibe un frame, intenta reconocer, y si corresponde, marca asistencia.
    """

    CONFIANZA_MINIMA = 0.6

    def __init__(
        self,
        reconocedor: ReconocedorFacialPort,
        repositorio_personas: RepositorioPersonasPort,
        repositorio_asistencia: RepositorioAsistenciaPort,
    ):
        self._reconocedor = reconocedor
        self._repositorio_personas = repositorio_personas
        self._repositorio_asistencia = repositorio_asistencia

    def ejecutar(self, imagen_bytes: bytes) -> ResultadoReconocimiento:
        personas_conocidas = self._repositorio_personas.listar_todas()
        resultado = self._reconocedor.reconocer(imagen_bytes, personas_conocidas)

        if not resultado.reconocido:
            return resultado

        if resultado.confianza < self.CONFIANZA_MINIMA:
            return resultado

        persona = resultado.persona
        if self._repositorio_asistencia.ya_registrado_hoy(persona.id):
            return resultado

        registro = RegistroAsistencia(
            persona_id=persona.id,
            nombre=persona.nombre,
            momento=datetime.now(),
            confianza=resultado.confianza,
        )
        self._repositorio_asistencia.registrar(registro)
        return resultado