from domain.ports.speech_recognizer import SpeechRecognizer
from domain.ports.speech_synthesizer import SpeechSynthesizer

from application.use_cases.saludar_inicialmente import SaludarInicialmente
from application.use_cases.informar_dia_semana import InformarDiaSemana
from application.use_cases.informar_hora import InformarHora
from application.use_cases.buscar_en_wikipedia import BuscarEnWikipedia
from application.use_cases.buscar_en_internet import BuscarEnInternet
from application.use_cases.reproducir_video import ReproducirVideo
from application.use_cases.contar_chiste import ContarChiste
from application.use_cases.consultar_precio_accion import ConsultarPrecioAccion
from application.use_cases.abrir_pagina_web import AbrirPaginaWeb
from application.use_cases.despedirse import Despedirse


class AsistenteController:

    def __init__(
            self,
            recognizer: SpeechRecognizer,
            synthesizer: SpeechSynthesizer,
            saludar_inicialmente: SaludarInicialmente,
            informar_dia_semana: InformarDiaSemana,
            informar_hora: InformarHora,
            buscar_en_wikipedia: BuscarEnWikipedia,
            buscar_en_internet: BuscarEnInternet,
            reproducir_video: ReproducirVideo,
            contar_chiste: ContarChiste,
            consultar_precio_accion: ConsultarPrecioAccion,
            abrir_pagina_web: AbrirPaginaWeb,
            despedirse: Despedirse,
    ):
        self._recognizer = recognizer
        self._synthesizer = synthesizer
        self._saludar_inicialmente = saludar_inicialmente
        self._informar_dia_semana = informar_dia_semana
        self._informar_hora = informar_hora
        self._buscar_en_wikipedia = buscar_en_wikipedia
        self._buscar_en_internet = buscar_en_internet
        self._reproducir_video = reproducir_video
        self._contar_chiste = contar_chiste
        self._consultar_precio_accion = consultar_precio_accion
        self._abrir_pagina_web = abrir_pagina_web
        self._despedirse = despedirse

    def iniciar(self) -> None:
        self._saludar_inicialmente.ejecutar()

        continuar = True
        while continuar:
            pedido = self._recognizer.escuchar().lower()
            continuar = self._procesar_comando(pedido)

    def _procesar_comando(self, pedido: str) -> bool:
        if 'abre youtube' in pedido:
            self._abrir_pagina_web.ejecutar(
                url='https://www.youtube.com/',
                mensaje_previo='Con gusto, Estoy abriendo youtube',
            )
        elif 'abre el navegador' in pedido:
            self._abrir_pagina_web.ejecutar(
                url='https://www.google.com/',
                mensaje_previo='Claro, estoy en eso',
            )
        elif 'qué día es hoy' in pedido:
            self._informar_dia_semana.ejecutar()
        elif 'qué hora es' in pedido:
            self._informar_hora.ejecutar()
        elif 'busca en wikipedia' in pedido:
            consulta = pedido.replace('busca en wikipedia', '').strip()
            self._buscar_en_wikipedia.ejecutar(consulta)
        elif 'busca en internet' in pedido:
            consulta = pedido.replace('busca en internet', '').strip()
            self._buscar_en_internet.ejecutar(consulta)
        elif 'reproduce' in pedido:
            self._reproducir_video.ejecutar(pedido)
        elif 'chiste' in pedido:
            self._contar_chiste.ejecutar()
        elif 'precio de las acciones' in pedido:
            nombre_empresa = pedido.split('de')[-1].strip()
            self._consultar_precio_accion.ejecutar(nombre_empresa)
        elif 'adiós' in pedido:
            self._despedirse.ejecutar()
            return False
        
        return True