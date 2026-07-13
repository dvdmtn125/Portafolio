from abc import ABC, abstractmethod


class SpeechSynthesizer(ABC):

    @abstractmethod
    def hablar(self, mensaje: str) -> None:
        raise NotImplementedError