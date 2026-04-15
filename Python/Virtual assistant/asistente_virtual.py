import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# Opciones voz / idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# Escuchar el micrófono y devolver el audio como texto
def transformar_audio_en_texto():

    # Almacenar recognizer en variable
    r = sr.Recognizer()

    # Configurar micrófono
    with sr.Microphone() as origen:

        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que comenzó la grabación
        print("Ya puedes hablar")

        # Guarda lo que escuche como audio
        audio = r.listen(origen)

        try:
            # Buscar en google
            pedido = r.recognize_google(audio, language="es-co")

            # Prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # Devolver pedido
            return pedido

        # En caso de que no comprenda el audio
        except sr.UnknownValueError:

            # Prueba de que no comprendió el audio
            print("No entendí")

            # Devolver error
            return "Sigo esperando"

        # En caso de no resolver el pedido
        except sr.RequestError:

            # Prueba de que no resolvío el pedido
            print("No hay servicio")

            # Devolver error
            return "Sigo esperando"

        # Error inesperado
        except:

            # Prueba de error inesperado
            print("Algo salio mal")

            # Devolver error
            return "Sigo esperando"


# Función para que el asistente pueda ser escuchado
def hablar(mensaje):

    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # Pronunciar el mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar el dia de la semana
def pedir_dia():

    # Crear variables con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # Crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario con nombres de días
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # Decir día de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# Informar la hora
def pedir_hora():

    # Crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # Decir la hora
    hablar(hora)


# Función de saludo inicial
def saludo_inicial():

    # Crear variable con datos hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 18:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 12:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

    # Decir saludo
    hablar(f'{momento}, soy Sabina, tu asistente personal. Por favor, dime en que te puedo ayudar')


# Función central del asistente
def pedir_cosas():

    # Saludo_inicial
    saludo_inicial()

    # Variable de corte
    comenzar = True

    # Loop central
    while comenzar:

        # Activar el micrófono y guardar el pedido en un String
        pedido = transformar_audio_en_texto().lower()

        if 'abre youtube' in pedido:
            hablar('Con gusto, Estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com/')
            continue
        elif 'abre el navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com/')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en Wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproduce' in pedido:
            hablar('Reproduciendo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'Esto fue lo que encontré, El precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('No pude encontrar la información solicitada')
                continue
        elif 'adiós' in pedido:
            despedida = datetime.datetime.now()
            if despedida.hour < 6 or despedida.hour > 18:
                adios = 'Feliz noche'
            elif 6 <= despedida.hour < 12:
                adios = 'Feliz día'
            else:
                adios = 'Feliz tarde'
            hablar(adios)
            break


pedir_cosas()
