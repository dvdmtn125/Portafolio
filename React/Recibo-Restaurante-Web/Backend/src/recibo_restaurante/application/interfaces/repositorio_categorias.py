from abc import ABC, abstractmethod

from recibo_restaurante.domain.categoria import Categoria


class RepositorioCategorias(ABC):
    @abstractmethod
    def listar(self) -> list[Categoria]:
        ...

    
    @abstractmethod
    def obtener_por_id(self, categoria_id: int) -> Categoria | None:
        ...


    @abstractmethod
    def crear(self, categoria: Categoria) -> Categoria:
        ...


    @abstractmethod
    def eliminar(self, categoria_id: int) -> None:
        """Lanza CategoriaConProductosAsociadosError si hay productos asociados."""
        ...