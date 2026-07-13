import cv2
import os
import face_recognition as fr
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parent.parent
ruta = RUTA_BASE / 'data' / 'empleados'

def cargar_empleados():
    
    #Crear base de datos de empleados
    mis_imagenes = []
    nombres_empleados = []
    lista_empleados = os.listdir(ruta)

    for nombre in lista_empleados:
        imagen = cv2.imread(str(ruta / nombre))
        mis_imagenes.append(imagen)
        nombres_empleados.append(os.path.splitext(nombre)[0])

    print(nombres_empleados)
    return mis_imagenes, nombres_empleados

#Codificar las imágenes de los empleados
def codificar_empleados(imagenes):
    lista_codificada = []
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        codificado = fr.face_encodings(imagen)[0]
        lista_codificada.append(codificado)
    return lista_codificada