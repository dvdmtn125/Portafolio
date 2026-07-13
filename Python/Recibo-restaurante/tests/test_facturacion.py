import pytest

from domain.facturacion import calcular_subtotal, calcular_totales, IVA_PORCENTAJE

# Calcular subtotal

def test_calcular_subtotal_un_producto():
    # 3 unidades a $1.32 cada una
    assert calcular_subtotal([3], [1.32]) == pytest.approx(3.96)

def test_calcular_subtotal_varios_productos():
    cantidades = [2, 1, 0]
    precios = [1.32, 1.65, 2.31]
    # 2*1.32 + 1*1.65 + 0*2.31 = 2.64 + 1.65 + 0 = 4.29
    assert calcular_subtotal(cantidades, precios) == pytest.approx(4.29)

def test_calcular_subtotal_sin_productos_seleccionados():
    assert calcular_subtotal([0, 0, 0], [1.32, 1.65, 2.31]) == 0

def test_calcular_subtotal_longitudes_distintas_lanza_error():
    with pytest.raises(ValueError):
        calcular_subtotal([1, 2], [1.32])

# Calcular totales

def test_calcular_totales_estructura_basica():
    cantidades = {'comida': [1], 'bebida': [0], 'postres': [0]}
    precios = {'comida': [10.0], 'bebida': [2.0], 'postres': [3.0]}

    resultado = calcular_totales(cantidades, precios)

    assert resultado['comida'] == 10.0
    assert resultado['bebida'] == 0
    assert resultado['postres'] == 0
    assert resultado['subtotal'] == 10.0

def test_calcular_totales_aplica_iva_correctamente():
    cantidades = {'comida': [1], 'bebida': [0], 'postres': [0]}
    precios = {'comida': [100.0], 'bebida': [2.0], 'postres': [3.0]}

    resultado = calcular_totales(cantidades, precios)

    assert resultado['subtotal'] == 100.0
    assert resultado['iva'] == pytest.approx(100.0 * IVA_PORCENTAJE)
    assert resultado['total'] == pytest.approx(119.0)

def test_calcular_totales_suma_varias_categorias():
    cantidades = {'comida': [2], 'bebida': [3], 'postres': [1]}
    precios = {'comida': [10.0], 'bebida': [2.0], 'postres': [5.0]}
    # subtotal = 20 + 6 + 5 = 31
    # iva = 31 * 0.19 = 5.89
    # total = 31 + 5.89 = 36.89

    resultado = calcular_totales(cantidades, precios)

    assert resultado['subtotal'] == pytest.approx(31.0)
    assert resultado['iva'] == pytest.approx(5.89)
    assert resultado['total'] == pytest.approx(36.89)

def test_calcular_totales_redondea_a_dos_decimales():
    cantidades = {'comida': [1], 'bebida': [0], 'postres': [0]}
    precios = {'comida': [1.005], 'bebida': [0], 'postres': [0]}

    resultado = calcular_totales(cantidades, precios)

    assert resultado['comida'] == round(resultado['comida'], 2)

def test_calcular_totales_categorias_no_coinciden_lanza_error():
    cantidades = {'comida': [1], 'bebida': [0]}
    precios = {'comida': [10.0], 'bebida': [2.0], 'postres': [3.0]}

    with pytest.raises(ValueError):
        calcular_totales(cantidades, precios)

def test_calcular_totales_sin_nada_seleccionado():
    cantidades = {'comida': [0, 0], 'bebida': [0], 'postres': [0]}
    precios = {'comida': [1.32, 1.65], 'bebida': [0.25], 'postres': [1.54]}

    resultado = calcular_totales(cantidades, precios)

    assert resultado['subtotal'] == 0
    assert resultado['iva'] == 0
    assert resultado['total'] == 0
