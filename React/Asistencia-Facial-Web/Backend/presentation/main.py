import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

from contextlib import asynccontextmanager
from io import BytesIO
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="face_recognition_models")

import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from infrastructure.deepface_liveness_adapter import DeepfaceAntispoofingAdapter
from presentation.routers import asistencia, personas

ORIGENES_PERMITIDOS = [os.getenv("FRONTEND_URL", "http://localhost:5173")]


def _generar_imagen_dummy_bytes() -> bytes:
    imagen = Image.new("RGB", (320, 240), color=(0, 0, 0))
    buffer = BytesIO()
    imagen.save(buffer, format="JPEG")
    return buffer.getvalue()
 

@asynccontextmanager
async def lifespan(app: FastAPI):
    DeepfaceAntispoofingAdapter().analizar(_generar_imagen_dummy_bytes())
    yield

app = FastAPI(title="Asistencia Facial API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENES_PERMITIDOS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(personas.router)
app.include_router(asistencia.router)