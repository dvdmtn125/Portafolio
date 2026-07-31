from datetime import date, datetime

import pytest

from application.use_cases.consultar_asistencias import ConsultarAsistencias
from domain.entities import RegistroAsistencia
from tests.application.fakes import FakeRepositorioAsistencia


@pytest.fixture
def repositorio_asistencia():
    return FakeRepositorioAsistencia()


@pytest.fixture
def caso_de_uso(repositorio_asistencia):
    return ConsultarAsistencias(repositorio_asistencia)


class TestConsultarAsistencia:
    def test_consulta_con_fecha_explicita(self, caso_de_uso, repositorio_asistencia):
        fecha_objetivo = date(2026, 7, 15)
        registro = RegistroAsistencia(
            persona_id="p1",
            nombre="Ana Torres",
            momento=datetime(2026, 7, 15, 8, 30),
            confianza=0.9,
        )
        repositorio_asistencia.registrar(registro)

        resultado = caso_de_uso.ejecutar(fecha=fecha_objetivo)

        assert resultado == [registro]

    def test_usa_fecha_de_hoy_cuando_no_se_especifica(
        self, caso_de_uso, repositorio_asistencia
    ):
        registro_hoy = RegistroAsistencia(
            persona_id="p1",
            nombre="Ana Torres",
            momento=datetime.now(),
            confianza=0.9,
        )
        registro_otro_dia = RegistroAsistencia(
            persona_id="p2",
            nombre="Luis Rey",
            momento=datetime(2020, 1, 1, 9, 0),
            confianza=0.9,
        )
        repositorio_asistencia.registrar(registro_hoy)
        repositorio_asistencia.registrar(registro_otro_dia)

        resultado = caso_de_uso.ejecutar()

        assert resultado == [registro_hoy]

    def test_devuelve_lista_vacia_si_no_hay_registros_en_la_fecha(self, caso_de_uso):
        resultado = caso_de_uso.ejecutar(fecha=date(2099, 1, 1))
        assert resultado == []