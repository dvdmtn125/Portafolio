from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from application.use_cases.registrar_persona import (
    ErrorRegistroPersona,
    RegistrarPersona
)
from infrastructure.face_recognition_adapter import ErrorImagenInvalida
from presentation.dependencies import get_registrar_persona
from presentation.schemas import PersonaSalida

router = APIRouter(prefix="/personas", tags=["personas"])


@router.post("", response_model=PersonaSalida, status_code=201)
async def registrar_persona(
    id: str = Form(...),
    nombre: str = Form(...),
    imagen: UploadFile = File(...),
    caso_de_uso: RegistrarPersona = Depends(get_registrar_persona),
):
    imagen_bytes = await imagen.read()

    try:
        persona = caso_de_uso.ejecutar(id, nombre, imagen_bytes)
    except ErrorRegistroPersona as error:
        raise HTTPException(status_code=422, detail=str(error))
    except ErrorImagenInvalida as error:
        raise HTTPException(status_code=422, detail=str(error))

    return PersonaSalida(id=persona.id, nombre=persona.nombre)