import pywhatkit

from domain.ports.video_player import VideoPlayer


class PywhatkitVideoPlayer(VideoPlayer):

    def reproducir(self, consulta: str) -> None:
        pywhatkit.playonyt(consulta)