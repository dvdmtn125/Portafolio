from domain.ports.speech_synthesizer import SpeechSynthesizer
from domain.ports.web_launcher import WebLauncher


class AbrirPaginaWeb:

    def __init__(self, synthesizer: SpeechSynthesizer, web_launcher:WebLauncher):
        self._synthesizer = synthesizer
        self._web_launcher = web_launcher

    def ejecutar(self, url: str, mensaje_previo: str) -> None:
        self._synthesizer.hablar(mensaje_previo)
        self._web_launcher.abrir(url)