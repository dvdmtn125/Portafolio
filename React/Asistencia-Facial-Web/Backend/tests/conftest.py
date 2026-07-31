import numpy as np
import pytest
from sqlalchemy.orm import sessionmaker

from domain.entities import Persona
from infrastructure.sqlalchemy_repositories import Base, crear_engine_sqlite


@pytest.fixture
def session_factory(tmp_path):
    """Motor SQLite temporal, aislado por test, para no ensuciar la BD real del proyecto."""
    ruta_db = tmp_path / "test_asistencia.db"
    engine = crear_engine_sqlite(str(ruta_db))
    yield sessionmaker(bind=engine)
    Base.metadata.drop_all(engine)


@pytest.fixture
def encoding_valido() -> np.ndarray:
    """Encoding de 128 floats, dimensión real que devuelve face_recognition."""
    return np.random.rand(128).astype(np.float64)


@pytest.fixture
def persona_ejemplo(encoding_valido) -> Persona:
    return Persona(id="p1", nombre="Ana Torres", encoding_facial=encoding_valido)