import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.routers import asistencia, personas

ORIGENES_PERMITIDOS = [os.getenv("FRONTEND_URL", "http://localhost:5173")]

app = FastAPI(title="Asistencia Facial API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENES_PERMITIDOS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(personas.router)
app.include_router(asistencia.router)