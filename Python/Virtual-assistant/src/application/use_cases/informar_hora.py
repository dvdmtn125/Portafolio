import datetime

from domain.ports.speech_synthesizer import SpeechSynthesizer


class InformarHora:

    def __init__(self, synthesizer: SpeechSynthesizer):
        self._synthesizer = synthesizer

    def ejecutar(self) -> None:
        ahora = datetime.datetime.now()
        mensaje = (
            f'En este momento son las {ahora.hour} horas '
            f'con {ahora.minute} minutos y {ahora.second} segundos'
        )
        self._synthesizer.hablar(mensaje)