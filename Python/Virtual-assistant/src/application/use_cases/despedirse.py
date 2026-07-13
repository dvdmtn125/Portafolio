import datetime

from domain.ports.speech_synthesizer import SpeechSynthesizer


class Despedirse:

    def __init__(self, synthesizer: SpeechSynthesizer):
        self._synthesizer = synthesizer

    def ejecutar(self) -> None:
        hora = datetime.datetime.now().hour
        if hora < 6 or hora > 18:
            mensaje = 'Feliz noche'
        elif 6 <= hora < 12:
            mensaje = 'Feliz día'
        else:
            mensaje = 'Feliz tarde'
        self._synthesizer.hablar(mensaje)