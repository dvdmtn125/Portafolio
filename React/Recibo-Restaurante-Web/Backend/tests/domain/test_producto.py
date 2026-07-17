import pytest

from recibo_restaurante.domain.producto import Producto


def test_producto_valido_se_crea_sin_error():
    producto = Producto(nombre='Limonada', precio=5000, categoria_id=1)
    assert producto.nombre == 'Limonada'
    assert producto.id is None


def test_producto_nombre_vacio_lanza_error():
    with pytest.raises(ValueError):
        Producto(nombre='', precio=5000, categoria_id=1)


def test_producto_precio_cero_lanza_error():
    with pytest.raises(ValueError):
        Producto(nombre='Limonada', precio=0, categoria_id=1)


def test_producto_precio_negativo_lanza_error():
    with pytest.raises(ValueError):
        Producto(nombre='Limonada', precio=-100, categoria_id=1)


def test_producto_categoria_id_invalido_lanza_error():
    with pytest.raises(ValueError):
        Producto(nombre='Limonada', precio=5000, categoria_id=0)