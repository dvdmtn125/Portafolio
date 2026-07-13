import platform
import cv2
import numpy as np
import face_recognition as fr


def iniciar_camara(indice=0):
    if platform.system() == 'Windows':
         return cv2.VideoCapture(indice, cv2.CAP_DSHOW)
    return cv2.VideoCapture(indice)

def buscar_coincidencia(codificacion_cara, codificacion_empleados, umbral=0.6):
     # Devueve el indice del empleado mas parecido, o None si no hay coincidencia
    distancias = fr.face_distance(codificacion_empleados, codificacion_cara)
    indice = np.argmin(distancias)

    if distancias[indice] > umbral:
        return None
    return indice

def dibujar_etiqueta(imagen, ubicacion_cara, nombre):
    y1, x2, y2,x1 = ubicacion_cara
    cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.rectangle(imagen, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
    cv2.putText(imagen, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)