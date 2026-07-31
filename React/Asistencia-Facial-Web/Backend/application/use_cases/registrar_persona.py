from domain.entities import Persona
from domain.ports import ReconocedorFacialPort, RepositorioPersonasPort


class ErrorRegistroPersona(Exception):
    """Se lanza cuando no se puede registrar una persona nueva"""


class RegistrarPersona:
    def __init__(
        self,
        reconocedor: ReconocedorFacialPort,
        repositorio_personas: RepositorioPersonasPort,
    ):
        self._reconocedor = reconocedor
        self._repositorio_personas = repositorio_personas

    def ejecutar(self, persona_id: str, nombre: str, imagen_bytes: bytes) -> Persona:
        encoding = self._reconocedor.calcular_encoding(imagen_bytes)
        if encoding is None:
            raise ErrorRegistroPersona(
                "No se detectó ningún rostro en la imagen proporcionada."
            )

        persona = Persona(id=persona_id, nombre=nombre, encoding_facial=encoding)
        self._repositorio_personas.guardar(persona)
        return persona