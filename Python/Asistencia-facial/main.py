import argparse
import cv2
import face_recognition as fr
import numpy as np

from src.comparar import comparar_fotos
from src.empleados import cargar_empleados, codificar_empleados
from src.registro import registrar_acesso
from src.camara import iniciar_camara, buscar_coincidencia, dibujar_etiqueta

def ejecutar_asistencia():
    #Cargar empleados y codificar sus caras
    imagenes, nombres_empleados = cargar_empleados()
    lista_codificada_empleados = codificar_empleados(imagenes)

    #Iniciar cámara
    captura = iniciar_camara()
    exito, imagen = captura.read()

    if not exito:
        print("No se pudo iniciar la cámara")
        return
    
    #Detectar caras en la imagen capturada
    cara_captura = fr.face_locations(imagen)

    #Codificar las caras detectadas
    codificacion_cara_captura = fr.face_encodings(imagen, cara_captura)

    #Buscar coincidencias para cada cara detectada
    for cara_codificada, cara_ubicacion in zip(codificacion_cara_captura, cara_captura):
        coincidencias = fr.compare_faces(lista_codificada_empleados, cara_codificada)
        distancias = fr.face_distance(lista_codificada_empleados, cara_codificada)

        print(distancias)

        indice_coincidencia = np.argmin(distancias)

        #Mostrar coincidencia si la hay
        if distancias[indice_coincidencia] > 0.6:
            print("No coincide con ningún empleado")
        else:
            nombre_empleado = nombres_empleados[indice_coincidencia]
            
            y1, x2, y2, x1 = cara_ubicacion
            cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(imagen, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(imagen, nombre_empleado, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            registrar_acesso(nombre_empleado)

    cv2.imshow('Asistencia', imagen)
    cv2.waitKey(0)

def main():
    parser = argparse.ArgumentParser(
        description="Sistema de asistencia por reconocimiento facial"
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    subparsers.add_parser(
        "asistencia",
        help="Ejecuta el reconocimiento facial con la cámara y registra el ingreso"
    )

    parser_comparar = subparsers.add_parser(
        "comparar",
        help="Compara dos fotos puntuales (demo de reconocimiento facial)"
    )
    parser_comparar.add_argument("foto_a", help="Nombre de la primera foto en data/img/")
    parser_comparar.add_argument("foto_b", help="Nombre de la segunda foto en data/img/")

    args = parser.parse_args()

    if args.comando == "asistencia":
        ejecutar_asistencia()
    elif args.comando == "comparar":
        comparar_fotos(args.foto_a, args.foto_b)


if __name__ == "__main__":
    main()  
