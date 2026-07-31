from functools import lru_cache

from sqlalchemy.orm import sessionmaker

from application.use_cases.consultar_asistencias import ConsultarAsistencias
from application.use_cases.reconocer_y_marcar_asistencia import (
    ReconocerYMarcarAsistencia,
)
from application.use_cases.registrar_persona import RegistrarPersona
from infrastructure.face_recognition_adapter import FaceRecognitionAdapter
from infrastructure.sqlalchemy_repositories import (
    RepositorioAsistenciaSQLAlchemy,
    RepositorioPersonasSQLAlchemy,
    crear_engine_sqlite,
)


@lru_cache
def _session_factory() -> sessionmaker:
    engine = crear_engine_sqlite()
    return sessionmaker(bind=engine)


@lru_cache
def _reconocedor() -> FaceRecognitionAdapter:
    return FaceRecognitionAdapter()


@lru_cache
def _repositorio_personas() -> RepositorioPersonasSQLAlchemy:
    return RepositorioPersonasSQLAlchemy(_session_factory())


@lru_cache
def _repositorio_asistencia() -> RepositorioAsistenciaSQLAlchemy:
    return RepositorioAsistenciaSQLAlchemy(_session_factory())


def get_registrar_persona() -> RegistrarPersona:
    return RegistrarPersona(_reconocedor(), _repositorio_personas())


def get_reconocer_y_marcar_asistencia() -> ReconocerYMarcarAsistencia:
    return ReconocerYMarcarAsistencia(
        _reconocedor(), _repositorio_personas(), _repositorio_asistencia()
    )


def get_consultar_asistencias() -> ConsultarAsistencias:
    return ConsultarAsistencias(_repositorio_asistencia())