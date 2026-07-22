from datetime import datetime

from recibo_restaurante.domain import recibo


def test_generar_numero_recibo_tiene_formato_esperado():
    numero = recibo.generar_numero_recibo()
    assert numero.startswith('N# - ')


def test_formatear_fecha_con_fecha_conocida():
    fecha = datetime(2026, 7, 17, 14, 30)
    resultado = recibo.formatear_fecha(fecha)
    assert resultado == '17/7/2026 - 14:30'


def test_generar_recibo_incluye_items_con_cantidad_mayor_a_cero():
    items = {'comida': [('Bandeja Paisa', '2', 15000.0)]}
    calculo = {'comida': 30000, 'bebida': 0, 'postres': 0, 'subtotal': 30000, 'iva': 5700, 'total': 35700}

    texto = recibo.generar_recibo(items, calculo, numero_recibo='N# - 1234', fecha=datetime(2026, 7, 17, 14, 30))

    assert 'Bandeja Paisa' in texto
    assert '$ 30000.0' in texto


def test_generar_recibo_excluye_items_con_cantidad_cero():
    items = {'comida': [('Bandeja Paisa', '0', 15000.0)]}
    calculo = {'comida': 0, 'bebida': 0, 'postres': 0, 'subtotal': 0, 'iva': 0, 'total': 0}

    texto = recibo.generar_recibo(items, calculo, numero_recibo='N# - 1234', fecha=datetime(2026, 7, 17, 14, 30))

    assert 'Bandeja Paisa' not in texto


def test_generar_recibo_incluye_totales():
    items = {}
    calculo = {'comida': 0, 'bebida': 0, 'postres': 0, 'subtotal': 0, 'iva': 0, 'total': 41650}

    texto = recibo.generar_recibo(items, calculo, numero_recibo='N# - 1234', fecha=datetime(2026, 7, 17, 14, 30))

    assert 'Total :' in texto
    assert '41650' in texto

def test_generar_recibo_soporta_categorias_dinamicas():
    calculo = {'bebidas': 5000, 'snacks': 3000, 'subtotal': 8000, 'iva': 1520, 'total': 9520}

    texto = recibo.generar_recibo({}, calculo, numero_recibo='N# - 1234', fecha=datetime(2026, 7, 17, 14, 30))

    assert 'Costo de Bebidas:' in texto
    assert 'Costo de Snacks:' in texto
    assert 'Total :' in texto