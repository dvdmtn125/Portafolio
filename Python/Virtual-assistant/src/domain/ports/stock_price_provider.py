from abc import ABC, abstractmethod


class StockPriceProvider(ABC):

    @abstractmethod
    def obtener_precio(self, simbolo: str) -> float:
        raise NotImplementedError