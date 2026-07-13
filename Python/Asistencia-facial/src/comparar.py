import cv2
import face_recognition as fr
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parent.parent
ruta = RUTA_BASE / 'data' / 'img'


def comparar_fotos(nombre_foto_control, nombre_foto_prueba):
    # Cargar imagen de prueba
    foto_control = fr.load_image_file(str(ruta / nombre_foto_control))
    foto_prueba = fr.load_image_file(str(ruta / nombre_foto_prueba))

    # Pasar fotos a RGB
    foto_control = cv2.cvtColor(foto_control, cv2.COLOR_BGR2RGB)
    foto_prueba = cv2.cvtColor(foto_prueba, cv2.COLOR_BGR2RGB)

    # Localizar cara en la imagen de control
    lugar_cara_control = fr.face_locations(foto_control)[0]
    codificacion_cara_control = fr.face_encodings(foto_control)[0]

    # Localizar cara en la imagen de prueba
    lugar_cara_prueba = fr.face_locations(foto_prueba)[0]
    codificacion_cara_prueba = fr.face_encodings(foto_prueba)[0]

    # Mostrar rectángulo en las caras
    cv2.rectangle(foto_control, (lugar_cara_control[3], lugar_cara_control[0]),
                  (lugar_cara_control[1], lugar_cara_control[2]), (0, 255, 0), 2)

    cv2.rectangle(foto_prueba, (lugar_cara_prueba[3], lugar_cara_prueba[0]),
                  (lugar_cara_prueba[1], lugar_cara_prueba[2]), (0, 255, 0), 2)

    # Comparar las caras
    resultado = fr.compare_faces([codificacion_cara_control], codificacion_cara_prueba)
    distancia = fr.face_distance([codificacion_cara_control], codificacion_cara_prueba)

    # Mostrar resultado
    cv2.putText(foto_prueba, f'{resultado} {distancia.round(2)}',
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Mostrar imágenes
    cv2.imshow('Foto Control', foto_control)
    cv2.imshow('Foto Prueba', foto_prueba)
    cv2.waitKey(0)
