from abc import ABC, abstractmethod


class SpeechRecognizer(ABC):

    @abstractmethod
    def escuchar(self) -> str:
        raise NotImplementedError