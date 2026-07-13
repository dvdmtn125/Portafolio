import pytest

from domain.calculadora import Calculadora


def test_inicia_vacio():
    calc = Calculadora()
    assert calc.expresion_actual == ''

def test_agregar_acumula_la_expresion():
    calc = Calculadora()
    calc.agregar('1')
    calc.agregar('2')
    calc.agregar('+')
    calc.agregar('3')
    assert calc.expresion_actual == '12+3'

def test_borrar_limpia_la_aexpresion():
    calc = Calculadora()
    calc.agregar('99')
    calc.borrar()
    assert calc.expresion_actual == ''

def test_calcular_suma():
    calc = Calculadora()
    calc.agregar('2')
    calc.agregar('+')
    calc.agregar('3')
    assert calc.calcular() == '5'

def test_calcular_multiplicacion():
    calc = Calculadora()
    calc.agregar('4')
    calc.agregar('*')
    calc.agregar('5')
    assert calc.calcular() == '20'

def test_calcular_reinicia_la_expresion():
    calc = Calculadora()
    calc.agregar('1')
    calc.agregar('+')
    calc.agregar('1')
    calc.calcular()
    assert calc.expresion_actual == ''

def test_calcular_expresion_vacia_lanza_error():
    calc = Calculadora()
    with pytest.raises(ValueError):
        calc.calcular()

def test_calcular_division_por_cero_lanza_error():
    calc = Calculadora()
    calc.agregar('8')
    calc.agregar('/')
    calc.agregar('0')
    with pytest.raises(ValueError):
        calc.calcular()

def test_calcular_caracteres_no_permitidos_lanza_error():
    calc = Calculadora()
    calc.agregar('import os')
    with pytest.raises(ValueError):
        calc.calcular()