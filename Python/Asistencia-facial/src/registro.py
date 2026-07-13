from pathlib import Path
from datetime import datetime

RUTA_BASE = Path(__file__).resolve().parent.parent
ruta = RUTA_BASE / 'data' / 'files' / 'registro.csv'


def registrar_acesso(persona, ruta_base=ruta):
    with open(ruta_base, 'r+') as f:
        lista_registro = f.readlines()
        nombres_registro = []
        for linea in lista_registro:
            entrada = linea.split(',')
            nombres_registro.append(entrada[0])

        if persona not in nombres_registro:
            ahora = datetime.now()
            dt_string = ahora.strftime('%Y-%m-%d %H:%M:%S')
            f.writelines(f'\n{persona},{dt_string}')