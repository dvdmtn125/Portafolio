from abc import ABC, abstractmethod


class WebLauncher(ABC):

    @abstractmethod
    def abrir(self, url: str) -> None:
        raise NotImplementedError