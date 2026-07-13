import io

from infrastructure.almacenamiento import guardar_recibo

class ArchivoFalso(io.StringIO):
    def __init__(self):
        super().__init__()
        self.cerrado = False
        self.contenido_guardado = ''

    def close(self):
        self.contenido_guardado = self.getvalue()
        self.cerrado = True
        super().close()


def test_guardar_recibo_escribe_el_contenido():
    archivo_falso = ArchivoFalso()

    resultado = guardar_recibo('contenido del recibo', abrir_dialogo=lambda: archivo_falso)

    assert resultado is True
    assert archivo_falso.contenido_guardado == 'contenido del recibo'

def test_guardar_recibo_cierra_el_archivo():
    archivo_falso = ArchivoFalso()

    guardar_recibo('contenido del recibo', abrir_dialogo=lambda: archivo_falso)

    assert archivo_falso.cerrado is True

def test_guardar_recibo_usuario_cancela_dialogo():
    resultado = guardar_recibo('contenido del recibo', abrir_dialogo=lambda: None)

    assert resultado is False

def test_guardar_recibo_escribe_contenido_vacio():
    archivo_falso = ArchivoFalso()

    resultado = guardar_recibo('', abrir_dialogo=lambda: archivo_falso)

    assert resultado is True
    assert archivo_falso.contenido_guardado == ''