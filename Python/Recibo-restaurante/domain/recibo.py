import random
from datetime import datetime

SEPARADOR_ANCHO = 54
SEPARADOR_ESTRELLAS = 47


def generar_numero_recibo():
    return f'N# - {random.randint(1000, 9999)}'

def formatear_fecha(fecha):
    return f'{fecha.day}/{fecha.month}/{fecha.year} - {fecha.hour}:{fecha.minute}'

def generar_recibo(items, calculo, numero_recibo=None, fecha=None):
    if numero_recibo is None:
        numero_recibo = generar_numero_recibo()
    if fecha is None:
        fecha = datetime.now()

    lineas = [
        f'Datos:\t{numero_recibo}\t\t{formatear_fecha(fecha)}',
        '*' * SEPARADOR_ESTRELLAS,
        'item\t\tCant.\tCosto Items',
        '-' * SEPARADOR_ANCHO,
    ]

    for categoria_items in items.values():
        for nombre, cantidad, precio_unitario in categoria_items:
            if cantidad != '0':
                costo = round(float(cantidad) * precio_unitario, 2)
                lineas.append(f'{nombre}\t\t{cantidad}\t$ {costo}')

    lineas.append('-' * SEPARADOR_ANCHO)
    lineas.append(f'Costo de la Comida: \t\t\t${calculo["comida"]}')
    lineas.append(f'Costo de la Bebida: \t\t\t${calculo["bebida"]}')
    lineas.append(f'Costo de la Postres: \t\t\t${calculo["postres"]}')
    lineas.append('-' * SEPARADOR_ANCHO)
    lineas.append(f'Subtotal :\t\t\t${calculo["subtotal"]}')
    lineas.append(f'Iva :\t\t\t${calculo["iva"]}')
    lineas.append(f'Total :\t\t\t${calculo["total"]}')
    lineas.append('-' * SEPARADOR_ANCHO)
    lineas.append('Lo esperamos pronto.')

    return '\n'.join(lineas)