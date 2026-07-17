import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from recibo_restaurante.composicion import obtener_sesion
from recibo_restaurante.infrastructure.db.modelos import Base
from recibo_restaurante.main import app



@pytest.fixture
def sesion_bd():
    motor = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=motor)
    SesionPrueba = sessionmaker(bind=motor)
    sesion = SesionPrueba()
    yield sesion
    sesion.close()
    motor.dispose()


@pytest.fixture
def cliente(sesion_bd):
    def _sesion_de_prueba():
        yield sesion_bd

    app.dependency_overrides[obtener_sesion] = _sesion_de_prueba
    with TestClient(app) as cliente_prueba:
        yield cliente_prueba
    app.dependency_overrides.clear()