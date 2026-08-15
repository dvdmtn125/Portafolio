import io
import logging

import numpy as np
from deepface import DeepFace
from PIL import Image, UnidentifiedImageError

from domain.entities import ResultadoLiveness
from domain.ports import DetectorLivenessPort
from infrastructure.face_recognition_adapter import ErrorImagenInvalida


logger = logging.getLogger(__name__)


class DeepfaceAntispoofingAdapter(DetectorLivenessPort):
    def analizar(self, imagen_bytes: bytes) -> ResultadoLiveness:
        imagen = self._bytes_a_array(imagen_bytes)

        try:
            caras_detectadas = DeepFace.extract_faces(
                img_path=imagen,
                detector_backend="retinaface",
                anti_spoofing=True,
                enforce_detection=False,
            )
        except ValueError:
            return ResultadoLiveness(es_real=False, confianza=0.0)

        if not caras_detectadas:
            return ResultadoLiveness(es_real=False, confianza=0.0)

        cara_principal = caras_detectadas[0]
        es_real = bool(cara_principal.get("is_real", False))
        confianza = float(cara_principal.get("antispoof_score", 0.0))

        return ResultadoLiveness(es_real=es_real, confianza=confianza)

    @staticmethod
    def _bytes_a_array(imagen_bytes: bytes) -> np.ndarray:
        try:
            imagen_pil = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
        except UnidentifiedImageError as error:
            raise ErrorImagenInvalida("La imagen no puede ser procesada.") from error
        return np.array(imagen_pil) 