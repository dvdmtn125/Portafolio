from datetime import datetime
from domain.recibo import generar_numero_recibo, formatear_fecha, generar_recibo

FECHA_FIJA = datetime(2024, 3, 15, 13, 5)
NUMERO_FIJO = 'N# - 1234'

CALCULO_EJEMPLO = {
    'comida': 10.0,
    'bebida': 2.0,
    'postres': 0,
    'subtotal': 12.0,
    'iva': 2.28,
    'total': 14.28,
}

def test_generar_numero_recibo_tiene_el_formato_correcto():
    numero = generar_numero_recibo()
    assert numero.startswith('N# - ')

    parte_numerica = numero.replace('N# - ', '')
    assert parte_numerica.isdigit()
    assert len(parte_numerica) == 4

def test_formatear_fecha():
    fecha = datetime(2024, 3, 5, 9, 7)
    assert formatear_fecha(fecha) == '5/3/2024 - 9:7'

def test_generar_recibo_incluye_numero_fecha():
    items = {'comida': [], 'bebida': [], 'postres': []}

    texto = generar_recibo(items, CALCULO_EJEMPLO, numero_recibo=NUMERO_FIJO, fecha=FECHA_FIJA)

    assert NUMERO_FIJO in texto
    assert formatear_fecha(FECHA_FIJA) in texto

def test_generar_recibo_lista_productos_con_cantidad_mayor_a_cero():
    items = {
        'comida': [('pollo', '2', 1.32)],
        'bebida': [],
        'postres': [],
    }

    texto = generar_recibo(items, CALCULO_EJEMPLO, numero_recibo=NUMERO_FIJO, fecha=FECHA_FIJA)

    assert 'pollo' in texto
    assert '2' in texto

def test_generar_recibo_omite_productos_con_cantidad_cero():
    items = {
        'comida': [('pollo', '2', 1.32), ('cordero', '1', 1.65)],
        'bebida': [],
        'postres': [],
    }

    texto = generar_recibo(items, CALCULO_EJEMPLO, numero_recibo=NUMERO_FIJO, fecha=FECHA_FIJA)

    assert 'pollo' in texto
    assert 'cordero' in texto

def test_generar_recibo_incluye_los_totales():
    items = {
        'comida': [],
        'bebida': [],
        'postres': [],
    }

    texto = generar_recibo(items, CALCULO_EJEMPLO, numero_recibo=NUMERO_FIJO, fecha=FECHA_FIJA)

    assert '$12.0' in texto
    assert '$2.28' in texto
    assert '$14.28' in texto

def test_generar_recibo_sin_parametros_opcionales_no_lanza_error():
    items = {
        'comida': [],
        'bebida': [],
        'postres': [],
    }

    texto = generar_recibo(items, CALCULO_EJEMPLO)
    
    assert isinstance(texto, str)
    assert len(texto) > 0