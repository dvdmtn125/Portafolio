import base64
import binascii
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from application.use_cases.consultar_asistencias import ConsultarAsistencias
from application.use_cases.reconocer_y_marcar_asistencia import (
    ReconocerYMarcarAsistencia,
)
from infrastructure.face_recognition_adapter import ErrorImagenInvalida
from presentation.dependencies import (
    get_consultar_asistencias,
    get_reconocer_y_marcar_asistencia,
)
from presentation.schemas import ReconocimientoSalida, RegistroAsistenciaSalida

router = APIRouter(prefix="/asistencia", tags=["asistencia"])


class FrameEntrada(BaseModel):
    imagen_base64: str


@router.post("/reconocer", response_model=ReconocimientoSalida)
async def reconocer(
    frame: FrameEntrada,
    caso_de_uso: ReconocerYMarcarAsistencia = Depends(get_reconocer_y_marcar_asistencia),
):
    try:
        imagen_bytes = base64.b64decode(frame.imagen_base64)
    except binascii.Error:
        raise HTTPException(status_code=422, detail="Imagen base64 inválida.")

    try:
        resultado = caso_de_uso.ejecutar(imagen_bytes)
    except ErrorImagenInvalida as error:
        raise HTTPException(status_code=422, detail=str(error))

    return ReconocimientoSalida(
        reconocido=resultado.reconocido,
        persona_id=resultado.persona.id if resultado.persona else None,
        nombre=resultado.persona.nombre if resultado.persona else None,
        confianza=resultado.confianza,
    )


@router.get("", response_model=list[RegistroAsistenciaSalida])
async def listar_asistencias(
    fecha: date | None = None,
    caso_de_uso: ConsultarAsistencias = Depends(get_consultar_asistencias),
):
    registros = caso_de_uso.ejecutar(fecha)
    return [
        RegistroAsistenciaSalida(
            persona_id=r.persona_id,
            nombre=r.nombre,
            momento=r.momento,
            confianza=r.confianza,
        )
        for r in registros
    ]