from domain.ports.speech_synthesizer import SpeechSynthesizer
from domain.ports.joke_provider import JokeProvider


class ContarChiste:

    def __init__(self, synthesizer: SpeechSynthesizer, joke_provider: JokeProvider):
        self._synthesizer = synthesizer
        self._joke_provider = joke_provider

    def ejecutar(self) -> None:
        chiste = self._joke_provider.obtener_chiste()
        self._synthesizer.hablar(chiste)