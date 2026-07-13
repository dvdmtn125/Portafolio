from abc import ABC, abstractmethod


class WebSearcher(ABC):

    @abstractmethod
    def buscar(self, consulta: str) -> None:
        raise NotImplementedError