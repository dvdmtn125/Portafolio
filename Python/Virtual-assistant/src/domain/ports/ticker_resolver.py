from abc import ABC, abstractmethod
from typing import Optional


class TicketResolver(ABC):

    @abstractmethod
    def resolver(self, nombre_empresa: str) -> Optional[str]:
        raise NotImplementedError