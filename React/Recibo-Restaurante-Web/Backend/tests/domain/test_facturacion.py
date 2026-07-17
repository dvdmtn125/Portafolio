import pytest

from recibo_restaurante.domain import facturacion


def test_calcular_subtotal_multiplica_y_suma():
    resultado = facturacion.calcular_subtotal([2, 1], [15000, 5000])
    assert resultado == 35000


def test_calcular_subtotal_longitudes_distintas_lanza_error():
    with pytest.raises(ValueError):
        facturacion.calcular_subtotal([1, 2], [1000])


def test_calcular_totales_devuelve_desglose_completo():
    cantidades = {'comida': [2], 'bebida': [1]}
    precios = {'comida': [15000], 'bebida': [5000]}

    resultado = facturacion.calcular_totales(cantidades, precios)

    assert resultado['comida'] == 30000
    assert resultado['bebida'] == 5000
    assert resultado['subtotal'] == 35000
    assert resultado['iva'] == pytest.approx(6650)
    assert resultado['total'] == pytest.approx(41650)


def test_calcular_totales_categorias_distintas_lanza_error():
    with pytest.raises(ValueError):
        facturacion.calcular_totales(
            cantidades={'comida': [1]},
            precios={'bebida': [1000]},
        )