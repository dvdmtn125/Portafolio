import datetime

from domain.ports.speech_synthesizer import SpeechSynthesizer


class SaludarInicialmente:

    def __init__(self, synthesizer: SpeechSynthesizer):
        self._synthesizer = synthesizer

    def ejecutar(self) -> None:
        hora_actual = datetime.datetime.now().hour
        momento = self._obtener_momento_del_dia(hora_actual)
        mensaje = f'{momento}, soy Sabina, tu asistente personal. Por favor dime en que te puedo ayudar'
        self._synthesizer.hablar(mensaje)

    @staticmethod
    def _obtener_momento_del_dia(hora: int) -> str:
        if hora < 6 or hora > 18:
            return 'Buenas noches'
        elif 6 <= hora < 12:
            return 'Buenos días'
        else:
            return 'Buenas tardes'