import datetime

from domain.ports.speech_synthesizer import SpeechSynthesizer


class InformarDiaSemana:
    _CALENDARIO = {
        0: 'Lunes',
        1: 'Martes',
        2: 'Miércoles',
        3: 'Jueves',
        4: 'Viernes',
        5: 'Sábado',
        6: 'Domingo',
    }

    def __init__(self, synthesizer: SpeechSynthesizer):
        self._synthesizer = synthesizer

    def ejecutar(self) -> None:
        dia_semana = datetime.date.today().weekday()
        nombre_dia = self._CALENDARIO[dia_semana]
        self._synthesizer.hablar(f'Hoy es {nombre_dia}')