import io

import face_recognition
import numpy as np
from PIL import Image, UnidentifiedImageError

from domain.entities import Persona, ResultadoReconocimiento
from domain.ports import ReconocedorFacialPort


class ErrorImagenInvalida(Exception):
    """La imagen recibida no pudo ser decodificada."""


class FaceRecognitionAdapter(ReconocedorFacialPort):
    """Implementación concreta usando la librería face_recognition."""

    TOLERANCIA = 0.6

    def calcular_encoding(self, imagen_bytes: bytes) -> np.ndarray | None:
        imagen = self._bytes_a_array(imagen_bytes)
        ubicaciones = face_recognition.face_locations(imagen)

        if not ubicaciones:
            return None

        encoding = face_recognition.face_encodings(imagen, ubicaciones)
        return encoding[0]

    def reconocer(
        self, imagen_bytes, personas_conocidas: list[Persona]
    ) -> ResultadoReconocimiento:
        if not personas_conocidas:
            return ResultadoReconocimiento(persona=None, confianza=0.0)

        imagen = self._bytes_a_array(imagen_bytes)
        ubicaciones = face_recognition.face_locations(imagen)

        if not ubicaciones:
            return ResultadoReconocimiento(persona=None, confianza=0.0)

        encoding_desconocido = face_recognition.face_encodings(imagen, ubicaciones)[0]
        encodings_conocidos = [p.encoding_facial for p in personas_conocidas]

        distancias = face_recognition.face_distance(
            encodings_conocidos, encoding_desconocido
        )
        indice_mejor_match = int(np.argmin(distancias))
        mejor_distancia = distancias[indice_mejor_match]

        if mejor_distancia > self.TOLERANCIA:
            return ResultadoReconocimiento(persona=None, confianza=0.0)

        confianza = 1.0 - mejor_distancia
        persona_reconocida = personas_conocidas[indice_mejor_match]

        return ResultadoReconocimiento(persona=persona_reconocida, confianza=confianza)

    @staticmethod
    def _bytes_a_array(imagen_bytes: bytes) -> np.ndarray:
        """Convierte bytes crudos (recibidos por HTTP) a un array RGB que face_recognition entiende."""
        try: 
            imagen_pil = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
        except UnidentifiedImageError as error:
            raise ErrorImagenInvalida("La imagen no pudo ser procesada.") from error
        return np.array(imagen_pil)
