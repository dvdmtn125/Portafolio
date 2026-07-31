from datetime import date, datetime, timedelta

import numpy as np
import pytest

from domain.entities import Persona, RegistroAsistencia
from infrastructure.sqlalchemy_repositories import (
    DIMENSION_ENCODING,
    ErrorEncodingCorrupto,
    PersonaModel,
    RepositorioAsistenciaSQLAlchemy,
    RepositorioPersonasSQLAlchemy,
)


@pytest.fixture
def repositorio_personas(session_factory):
    return RepositorioPersonasSQLAlchemy(session_factory)


@pytest.fixture
def repositorio_asistencia(session_factory):
    return RepositorioAsistenciaSQLAlchemy(session_factory)


class TestRepositorioPersonasSQLAlchemy:
    def test_guarda_y_recupera_persona_con_encoding_intacto(
        self, repositorio_personas, persona_ejemplo
    ):
        repositorio_personas.guardar(persona_ejemplo)

        recuperada = repositorio_personas.buscar_por_id(persona_ejemplo.id)

        assert recuperada is not None
        assert recuperada.id == persona_ejemplo.id
        assert recuperada.nombre == persona_ejemplo.nombre

        np.testing.assert_array_equal(
            recuperada.encoding_facial, persona_ejemplo.encoding_facial
        )

    def test_buscar_por_id_devuelve_none_si_no_existe(self, repositorio_personas):
        assert repositorio_personas.buscar_por_id("no-existe") is None

    def test_listar_todas_devuelve_todas_las_personas_guardadas(
        self, repositorio_personas, encoding_valido
    ):
        persona_a = Persona(id="p1", nombre="Ana", encoding_facial=encoding_valido)
        persona_b = Persona(id="p2", nombre="Luis", encoding_facial=encoding_valido)

        repositorio_personas.guardar(persona_a)
        repositorio_personas.guardar(persona_b)

        todas = repositorio_personas.listar_todas()

        assert {p.id for p in todas} == {"p1", "p2"}

    def test_guardar_actualiza_si_el_id_ya_existe(
        self, repositorio_personas, encoding_valido
    ):
        persona_original = Persona(id="p1", nombre="Ana", encoding_facial=encoding_valido)
        repositorio_personas.guardar(persona_original)

        nuevo_encoding = np.random.rand(128).astype(np.float64)
        persona_actualizada = Persona(
            id="p1", nombre="Ana Torres", encoding_facial=nuevo_encoding
        )
        repositorio_personas.guardar(persona_actualizada)

        recuperada = repositorio_personas.buscar_por_id("p1")

        assert recuperada.nombre == "Ana Torres"
        np.testing.assert_array_equal(recuperada.encoding_facial, nuevo_encoding)
        assert len(repositorio_personas.listar_todas()) == 1

    def test_lanza_error_si_encoding_almacenado_tiene_dimension_incorrecta(
        self, repositorio_personas, session_factory
    ):
        with session_factory() as session:
            modelo = PersonaModel(
                id="corrupto",
                nombre="Dato Corrupto",
                encoding_facial=np.zeros(64).tobytes(),
            )
            session.add(modelo)
            session.commit()

        with pytest.raises(ErrorEncodingCorrupto):
            repositorio_personas.buscar_por_id("corrupto")


class TestRepositorioAsistenciaSQLAlchemy:
    def test_registrar_y_listar_por_fecha(self, repositorio_asistencia):
        hoy = date.today()
        registro = RegistroAsistencia(
            persona_id="p1",
            nombre="Ana Torres",
            momento=datetime.now(),
            confianza=0.9,
        )

        repositorio_asistencia.registrar(registro)
        resultado = repositorio_asistencia.listar_por_fecha(hoy)

        assert len(resultado) == 1
        assert resultado[0].persona_id == "p1"
        assert resultado[0].confianza == 0.9

    def test_listar_por_fecha_no_incluye_otros_dias(self, repositorio_asistencia):
        registro_ayer = RegistroAsistencia(
            persona_id="p1",
            nombre="Ana Torres",
            momento=datetime.now() - timedelta(days=1),
            confianza=0.9,
        )
        repositorio_asistencia.registrar(registro_ayer)

        resultado_hoy = repositorio_asistencia.listar_por_fecha(date.today())

        assert resultado_hoy == []

    def test_ya_registrado_hoy_es_false_si_no_hay_registro(self, repositorio_asistencia):
        assert repositorio_asistencia.ya_registrado_hoy("p1") is False

    def test_ya_registrado_hoy_es_true_despues_de_registrar(self, repositorio_asistencia):
        registro = RegistroAsistencia(
            persona_id="p1",
            nombre="Ana Torres",
            momento=datetime.now(),
            confianza=0.9,
        )
        repositorio_asistencia.registrar(registro)

        assert repositorio_asistencia.ya_registrado_hoy("p1") is True

    def test_ya_registrado_hoy_no_afecta_a_otras_personas(self, repositorio_asistencia):
        registro = RegistroAsistencia(
            persona_id="p1",
            nombre="Ana Torres",
            momento=datetime.now(),
            confianza=0.9,
        )
        repositorio_asistencia.registrar(registro)

        assert repositorio_asistencia.ya_registrado_hoy("p2") is False