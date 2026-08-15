from datetime import datetime

import pytest

from application.use_cases.reconocer_y_marcar_asistencia import (
    ReconocerYMarcarAsistencia
)
from domain.entities import ResultadoReconocimiento, ResultadoLiveness
from tests.application.fakes import (
    FakeDetectorLiveness,
    FakeReconocedorFacial,
    FakeRepositorioAsistencia,
    FakeRepositorioPersonas,
)


@pytest.fixture
def reconocedor():
    return FakeReconocedorFacial()


@pytest.fixture
def repositorio_personas():
    return FakeRepositorioPersonas()


@pytest.fixture
def repositorio_asistencia():
    return FakeRepositorioAsistencia()


@pytest.fixture
def detector_liveness():
    return FakeDetectorLiveness()


@pytest.fixture
def caso_de_uso(reconocedor, detector_liveness, repositorio_personas, repositorio_asistencia):
    return ReconocerYMarcarAsistencia(
        reconocedor, detector_liveness, repositorio_personas, repositorio_asistencia
    )


class TestReconocerYMarcarAsistencia:
    def test_marca_asistencia_cuando_reconoce_con_confianza_suficiente(
        self, caso_de_uso, reconocedor, persona_ejemplo, repositorio_asistencia
    ):
        reconocedor.resultado_a_devolver = ResultadoReconocimiento(
            persona=persona_ejemplo, confianza=0.9
        )

        resultado = caso_de_uso.ejecutar(b"frame de webcam")

        assert resultado.reconocido is True
        assert repositorio_asistencia.ya_registrado_hoy(persona_ejemplo.id) is True

    def test_no_marca_asistencia_si_no_hay_match(
        self, caso_de_uso, reconocedor, repositorio_asistencia
    ):
        reconocedor.resultado_a_devolver = ResultadoReconocimiento(
            persona=None, confianza=0.0
        )

        resultado = caso_de_uso.ejecutar(b"frame sin rostro conocido")

        assert resultado.reconocido is False
        assert repositorio_asistencia._registros == []

    def test_no_marca_asistencia_cuando_confianza_es_menor_al_minimo(
        self, caso_de_uso, reconocedor, persona_ejemplo, repositorio_asistencia
    ):
        confianza_baja = ReconocerYMarcarAsistencia.CONFIANZA_MINIMA - 0.1
        reconocedor.resultado_a_devolver = ResultadoReconocimiento(
            persona=persona_ejemplo, confianza=confianza_baja
        )

        resultado = caso_de_uso.ejecutar(b"frame con match dudoso")

        assert resultado.reconocido is True #El reconocedor si encontro un match...
        assert repositorio_asistencia.ya_registrado_hoy(persona_ejemplo.id) is False
        #... pero la regla de negocio no lo considera suficiente para marcar asistencia

    def test_no_marca_asistencia_duplicada_el_mismo_dia(
        self, caso_de_uso, reconocedor, persona_ejemplo, repositorio_asistencia
    ):
        reconocedor.resultado_a_devolver = ResultadoReconocimiento(
            persona= persona_ejemplo, confianza=0.9
        )

        caso_de_uso.ejecutar(b"primer frame")
        caso_de_uso.ejecutar(b"segundo frame, mismo rostro, segundo despues")

        registro_de_la_persona = [
            r for r in repositorio_asistencia._registros
            if r.persona_id == persona_ejemplo.id
        ]
        assert len(registro_de_la_persona) == 1

    def test_devuelve_confianza_exacta_del_reconocedor(
        self, caso_de_uso, reconocedor, persona_ejemplo
    ):
        reconocedor.resultado_a_devolver = ResultadoReconocimiento(
            persona=persona_ejemplo, confianza=0.87
        )

        resultado = caso_de_uso.ejecutar(b"frame")

        assert resultado.confianza == 0.87

    def test_no_reconoce_cuando_liveness_detecta_spoofing(
        self, caso_de_uso, reconocedor, detector_liveness, persona_ejemplo
    ):
        detector_liveness.resultado_a_devolver = ResultadoLiveness(
            es_real=False, confianza=0.9
        )
        reconocedor.resultado_a_devolver = ResultadoReconocimiento(
            persona=persona_ejemplo, confianza=0.9
        )

        resultado = caso_de_uso.ejecutar(b"foto de una foto")

        assert resultado.reconocido is False

    def test_no_reconoce_cuando_liveness_tiene_confianza_baja(
        self, caso_de_uso, reconocedor, detector_liveness, persona_ejemplo
    ):
        detector_liveness.resultado_a_devolver = ResultadoLiveness(
            es_real=True, confianza=0.3 # Por debajo de CONFIANZA_MINIMA_LIVENESS
        )
        reconocedor.resultado_a_devolver = ResultadoReconocimiento(
            persona=persona_ejemplo, confianza=0.9
        )

        resultado = caso_de_uso.ejecutar(b"imagen dudosa")

        assert resultado.reconocido is False

    def test_no_llama_reconocedor_si_liveness_rechaza_la_imagen(
            self, caso_de_uso, reconocedor, detector_liveness
        ):
            detector_liveness.resultado_a_devolver = ResultadoLiveness(
                es_real=False, confianza=0.9
            )
            
            resultado = caso_de_uso.ejecutar(b"foto de una foto")
    
            assert reconocedor.imagenes_recibidas == [] # nunca se llegó a intentar reonocer

    def test_reconoce_normalmente_cunado_liveness_aprueba(
            self, caso_de_uso, reconocedor, detector_liveness, persona_ejemplo
        ):
            detector_liveness.resultado_a_devolver = ResultadoLiveness(
                es_real=True, confianza=0.95
            )
            reconocedor.resultado_a_devolver = ResultadoReconocimiento(
                persona=persona_ejemplo, confianza=0.9
            )
    
            resultado = caso_de_uso.ejecutar(b"persona real")
    
            assert resultado.reconocido is True