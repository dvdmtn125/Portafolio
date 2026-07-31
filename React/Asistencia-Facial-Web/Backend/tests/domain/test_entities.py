import numpy as np
import pytest

from domain.entities import Persona, ResultadoReconocimiento


class TestPersona:
    def test_dos_personas_con_mismo_id_son_iguales(self):
        encoding_a = np.zeros(128)
        encoding_b = np.ones(128)

        persona_a = Persona(id="p1", nombre="Ana", encoding_facial=encoding_a)
        persona_b = Persona(id="p1", nombre="Ana Torres", encoding_facial=encoding_b)

        assert persona_a == persona_b

    def test_personas_con_id_distinto_no_son_iguales(self):
        encoding = np.zeros(128)
        persona_a = Persona(id="p1", nombre="Ana", encoding_facial=encoding)
        persona_b = Persona(id="p2", nombre="Ana", encoding_facial=encoding)

        assert persona_a != persona_b


class TestResultadoReconocimiento:
    def test_reconocido_es_true_cuando_hay_persona(self, persona_ejemplo):
        resultado = ResultadoReconocimiento(persona=persona_ejemplo, confianza=0.9)
        assert resultado.reconocido is True

    def test_reconocido_es_false_cuando_no_hay_persona(self):
        resultado = ResultadoReconocimiento(persona=None, confianza=0.0)
        assert resultado.reconocido is False