from abc import ABC, abstractmethod


class JokeProvider(ABC):

    @abstractmethod
    def obtener_chiste(self) -> str:
        raise NotImplementedError