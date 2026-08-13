from datetime import datetime

from config import CONFIANZA_MINIMA_LIVENESS
from domain.entities import RegistroAsistencia, ResultadoReconocimiento
from domain.ports import (
    DetectorLivenessPort,
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
        detector_liveness: DetectorLivenessPort,
        repositorio_personas: RepositorioPersonasPort,
        repositorio_asistencia: RepositorioAsistenciaPort,
    ):
        self._reconocedor = reconocedor
        self._detector_liveness = detector_liveness
        self._repositorio_personas = repositorio_personas
        self._repositorio_asistencia = repositorio_asistencia

    def ejecutar(self, imagen_bytes: bytes) -> ResultadoReconocimiento:
        resultado_liveness = self._detector_liveness.analizar(imagen_bytes)

        if not resultado_liveness.es_real or resultado_liveness.confianza < CONFIANZA_MINIMA_LIVENESS:
            return ResultadoReconocimiento(persona=None, confianza=0.0)

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