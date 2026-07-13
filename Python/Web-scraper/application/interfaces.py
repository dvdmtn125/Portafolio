from abc import ABC, abstractmethod
from typing import List

from domain.entities import Quote


class QuoteScraperPort(ABC):
    @abstractmethod
    def fetch_quotes(self, max_pages: int) -> List[Quote]:
        raise NotImplementedError
    

class QuoteRepositoryPort(ABC):
    @abstractmethod
    def save(self, quotes: List[Quote]) -> None:
        raise NotImplementedError