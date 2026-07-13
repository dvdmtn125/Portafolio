import numpy as np
import pytest

from src.camara import buscar_coincidencia, dibujar_etiqueta


# --- Tests para buscar_coincidencia ---

def test_buscar_coincidencia_encuentra_el_mas_cercano():
    """Si la cara coincide claramente con un empleado, debe devolver su índice."""
    codificacion_cara = np.array([0.1, 0.1, 0.1])
    codificacion_empleados = [
        np.array([0.9, 0.9, 0.9]),   # empleado 0: lejano
        np.array([0.1, 0.1, 0.15]),  # empleado 1: muy cercano
        np.array([0.5, 0.5, 0.5]),   # empleado 2: medio
    ]

    indice = buscar_coincidencia(codificacion_cara, codificacion_empleados)

    assert indice == 1


def test_buscar_coincidencia_sin_match_devuelve_none():
    """Si todas las distancias superan el umbral, no hay coincidencia válida."""
    codificacion_cara = np.array([10.0, 10.0, 10.0])
    codificacion_empleados = [
        np.array([0.0, 0.0, 0.0]),
        np.array([0.1, 0.1, 0.1]),
    ]

    indice = buscar_coincidencia(codificacion_cara, codificacion_empleados, umbral=0.6)

    assert indice is None


def test_buscar_coincidencia_respeta_el_umbral_personalizado():
    """Un umbral más permisivo debe aceptar una coincidencia que el umbral
    por defecto rechazaría."""
    codificacion_cara = np.array([0.0, 0.0, 0.0])
    codificacion_empleados = [np.array([0.5, 0.5, 0.5])]

    # Con el umbral por defecto (0.6) no debería haber coincidencia
    assert buscar_coincidencia(codificacion_cara, codificacion_empleados) is None

    # Con un umbral más amplio, sí debería encontrarla
    indice = buscar_coincidencia(codificacion_cara, codificacion_empleados, umbral=2.0)
    assert indice == 0


# --- Tests para dibujar_etiqueta ---

def test_dibujar_etiqueta_no_lanza_error():
    """dibujar_etiqueta debe poder ejecutarse sobre una imagen válida sin lanzar
    excepciones, dada una ubicación de cara y un nombre."""
    imagen = np.zeros((200, 200, 3), dtype=np.uint8)
    ubicacion_cara = (50, 150, 150, 50)  # y1, x2, y2, x1

    # No debería lanzar ninguna excepción
    dibujar_etiqueta(imagen, ubicacion_cara, "Empleado de Prueba")


def test_dibujar_etiqueta_modifica_la_imagen():
    """Tras dibujar el recuadro y el texto, la imagen ya no debe ser
    completamente negra (algo se dibujó encima)."""
    imagen = np.zeros((200, 200, 3), dtype=np.uint8)
    ubicacion_cara = (50, 150, 150, 50)

    dibujar_etiqueta(imagen, ubicacion_cara, "Empleado de Prueba")

    assert imagen.sum() > 0