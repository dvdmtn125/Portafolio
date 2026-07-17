import pytest

from recibo_restaurante.domain.categoria import Categoria


def test_categoria_valida_se_crea_sin_error():
    categoria = Categoria(nombre='Bebidas')
    assert categoria.nombre == 'Bebidas'
    assert categoria.id is None


def test_categoria_con_id_se_crea_correctamente():
    categoria = Categoria(nombre='Bebidas', id=5)
    assert categoria.id == 5


def test_categoria_nombre_vacio_lanza_error():
    with pytest.raises(ValueError):
        Categoria(nombre='')


def test_categoria_nombre_solo_espacios_lanza_error():
    with pytest.raises(ValueError):
        Categoria(nombre='    ')