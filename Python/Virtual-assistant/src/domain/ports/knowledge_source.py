from abc import ABC, abstractmethod


class KnowledgeSource(ABC):

    @abstractmethod
    def buscar_resumen(self, consulta: str) -> str:
        raise NotImplementedError