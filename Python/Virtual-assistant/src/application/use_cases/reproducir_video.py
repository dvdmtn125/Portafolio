from domain.ports.speech_synthesizer import SpeechSynthesizer
from domain.ports.video_player import VideoPlayer


class ReproducirVideo:

    def __init__(self, synthesizer: SpeechSynthesizer, video_player: VideoPlayer):
        self._synthesizer = synthesizer
        self._video_player = video_player

    def ejecutar(self, consulta: str) -> None:
        self._synthesizer.hablar('Reproduciendo')
        self._video_player.reproducir(consulta)