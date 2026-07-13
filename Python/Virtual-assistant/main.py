import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from infrastructure.pyttsx3_speech_synthesizer import Pyttsx3SpeechSynthesizer
from infrastructure.google_speech_recognizer import GoogleSpeechRecognizer
from infrastructure.wikipedia_knowledge_source import WikipediaKnowledgeSource
from infrastructure.pywhatkit_web_searcher import PywhatkitWebSearcher
from infrastructure.pywhatkit_video_player import PywhatkitVideoPlayer
from infrastructure.pyjokes_joke_provider import PyjokesJokeProvider
from infrastructure.webbrowser_web_launcher import WebbrowserWebLauncher
from infrastructure.yfinance_stock_price_provider import YfinanceStockPriceProvider
from infrastructure.yahoo_ticker_resolver import YahooTickerResolver

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

from controllers.asistente_controller import AsistenteController


def main() -> None:
    #1. Infraestructura
    synthesizer = Pyttsx3SpeechSynthesizer()
    recognizer = GoogleSpeechRecognizer()
    knowledge_source = WikipediaKnowledgeSource()
    web_searcher = PywhatkitWebSearcher()
    video_player = PywhatkitVideoPlayer()
    joke_provider = PyjokesJokeProvider()
    web_launcher = WebbrowserWebLauncher()
    stock_provider = YfinanceStockPriceProvider()
    ticker_resolver = YahooTickerResolver()

    #2. Aplicación: recibe la infraestructura
    saludar_inicialmente = SaludarInicialmente(synthesizer)
    informar_dia_semana = InformarDiaSemana(synthesizer)
    informar_hora = InformarHora(synthesizer)
    buscar_en_wikipedia = BuscarEnWikipedia(synthesizer,knowledge_source)
    buscar_en_internet = BuscarEnInternet(synthesizer,web_searcher)
    reproducir_video = ReproducirVideo(synthesizer, video_player)
    contar_chiste = ContarChiste(synthesizer, joke_provider)
    consultar_precio_accion = ConsultarPrecioAccion(synthesizer, stock_provider, ticker_resolver)
    abrir_pagina_web = AbrirPaginaWeb(synthesizer, web_launcher)
    despedirse = Despedirse(synthesizer)

    #3. Controller: recibe los casos de uso de la aplicación
    controller = AsistenteController(
        recognizer=recognizer,
        synthesizer=synthesizer,
        saludar_inicialmente=saludar_inicialmente,
        informar_dia_semana=informar_dia_semana,
        informar_hora=informar_hora,
        buscar_en_wikipedia=buscar_en_wikipedia,
        buscar_en_internet=buscar_en_internet,
        reproducir_video=reproducir_video,
        contar_chiste=contar_chiste,
        consultar_precio_accion=consultar_precio_accion,
        abrir_pagina_web=abrir_pagina_web,
        despedirse=despedirse,
    )

    #4. Iniciar
    controller.iniciar()



if __name__ == "__main__":
    main()
