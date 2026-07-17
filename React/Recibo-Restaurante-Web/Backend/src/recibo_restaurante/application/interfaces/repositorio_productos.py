from abc import ABC, abstractmethod

from recibo_restaurante.domain.producto import Producto


class RepositorioProductos(ABC):
    @abstractmethod
    def listar(self) -> list[Producto]:
        ...


    @abstractmethod
    def listar_por_categoria(self, categoria_id: int) -> list[Producto]:
        ...


    @abstractmethod
    def obtener_por_id(self, producto_id: int) -> Producto | None:
        ...


    @abstractmethod
    def crear(self, producto: Producto) -> Producto:
        ...


    @abstractmethod
    def actualizar(self, producto: Producto) -> Producto:
        ...


    @abstractmethod
    def eliminar(self, producto_id: int) -> None:
        ...