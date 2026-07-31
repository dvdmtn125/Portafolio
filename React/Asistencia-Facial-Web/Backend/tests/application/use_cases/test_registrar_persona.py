import numpy as np
import pytest

from application.use_cases.registrar_persona import (
    ErrorRegistroPersona,
    RegistrarPersona,
)
from tests.application.fakes import FakeReconocedorFacial, FakeRepositorioPersonas


@pytest.fixture
def reconocedor():
    return FakeReconocedorFacial()


@pytest.fixture
def repositorio_personas():
    return FakeRepositorioPersonas()


@pytest.fixture
def caso_de_uso(reconocedor, repositorio_personas):
    return RegistrarPersona(reconocedor, repositorio_personas)


class TestRegistrarPersonas:
    def test_registra_persona_cuando_se_detecta_rostro(
            self, caso_de_uso, repositorio_personas
    ):
        persona = caso_de_uso.ejecutar("p1", "Ana Torres", b"imagen falsa")

        assert persona.id == "p1"
        assert persona.nombre == "Ana Torres"
        assert repositorio_personas.buscar_por_id("p1") == persona

    def test_lanza_error_cuando_no_se_detecta_rostro(
            self, caso_de_uso, reconocedor, repositorio_personas
    ):
        reconocedor.encoding_a_devolver = None

        with pytest.raises(ErrorRegistroPersona):
            caso_de_uso.ejecutar("p1", "Ana Torres", b"imagen sin rostro")

        assert repositorio_personas.buscar_por_id("p1") is None

    def test_no_guarda_nada_si_falla_la_deteccion(
            self, caso_de_uso, reconocedor, repositorio_personas
    ):
        reconocedor.encoding_a_devolver = None

        with pytest.raises(ErrorRegistroPersona):
            caso_de_uso.ejecutar("p1", "Ana Torres", b"imagen sin rostro")

        assert repositorio_personas.listar_todas() == []