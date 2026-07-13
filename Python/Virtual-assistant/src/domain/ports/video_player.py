from abc import ABC, abstractmethod


class VideoPlayer(ABC):

    @abstractmethod
    def reproducir(self, consulta: str) -> None:
        raise NotImplementedError