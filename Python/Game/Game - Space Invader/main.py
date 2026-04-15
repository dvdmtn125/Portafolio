import pygame
import os
import random
import math
from pygame import mixer
import io

# Inicializar a pygame
pygame.init()

# Crear reloj para limitar FPS
clock = pygame.time.Clock()


# Función para pasar las fuentes a bytes
def fuente_bytes(font):
    with open(font, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption("Space Invaders")
ruta_icono = os.path.join("Img", "ovni.png")
icono = pygame.image.load(ruta_icono)
pygame.display.set_icon(icono)
ruta_fondo = os.path.join("Img", "Fondo.jpg")
fondo = pygame.image.load(ruta_fondo)

# Agregar música
ruta_musica = os.path.join("sonidos", "MusicaFondo.mp3")
mixer.music.load(ruta_musica)
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Variables del jugador
ruta_jugador = os.path.join("Img", "cohete.png")
img_jugador = pygame.image.load(ruta_jugador)
# (Ancho /2) - (img_jugador/2)
jugador_x = 368
# Alto - img_jugador
jugador_y = 500
# Movimiento del jugador en x
jugador_x_cambio = 0

# Variables del enemigo
ruta_enemigo = os.path.join("Img", "enemigo.png")
img_enemigo = []
enemigo_x = []
enemigo_y = []
# Movimiento horizontal y vertical del enemigo
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load(ruta_enemigo))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    # Movimiento horizontal y vertical del enemigo
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)


# Variables del la bala
balas = []
ruta_bala = os.path.join("Img", "bala.png")
img_bala = pygame.image.load(ruta_bala)
bala_x = 0
bala_y = 500
# Movimiento vertical de la bala
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False


# Puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes("FreeSansBold.ttf")
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y = 10


# texto final del juego
fuente_final = pygame.font.Font(fuente_como_bytes, 50)


# Texto de game over
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (160, 250))


# Función mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Función llamada jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Función llamada enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Función disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# Función detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
execute = True
while execute:

    # RGB de la pantalla
    pantalla.blit(fondo, (0, 0))
    pygame.time.delay(2)

    # Iterar eventos
    for event in pygame.event.get():

        # Evento cerrar
        if event.type == pygame.QUIT:
            execute = False

        # Evento presionar flechas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if event.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if event.key == pygame.K_SPACE:
                ruta_sonido_bala = os.path.join("sonidos", "disparo.mp3")
                sonido_bala = mixer.Sound(ruta_sonido_bala)
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        # Evento soltar flechas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicación del jugador
    jugador_x += jugador_x_cambio

    # Mantener dentro de bordes del jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicación del enemigo
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 430:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # Mantener dentro de bordes del enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colisión
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                ruta_colision = os.path.join("sonidos", "Golpe.mp3")
                sonido_colision = mixer.Sound(ruta_colision)
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento Bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)

    # Mostrar puntaje
    mostrar_puntaje(texto_x, texto_y)

    # Actualizar // Update
    pygame.display.update()

    # Limitar FPS
    clock.tick(120)
