from domain.ports.speech_synthesizer import SpeechSynthesizer
from domain.ports.web_searcher import WebSearcher


class BuscarEnInternet:

    def __init__(self, synthesizer: SpeechSynthesizer, web_searcher: WebSearcher):
        self._synthesizer = synthesizer
        self._web_searcher = web_searcher

    def ejecutar(self, consulta: str) -> None:
        self._synthesizer.hablar('Ya mismo estoy en eso')
        self._web_searcher.buscar(consulta)
        self._synthesizer.hablar('Esto es lo que he encontrado')