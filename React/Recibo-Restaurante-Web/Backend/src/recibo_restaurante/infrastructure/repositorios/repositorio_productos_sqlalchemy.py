from sqlalchemy.orm import Session

from recibo_restaurante.application.interfaces.repositorio_productos import RepositorioProductos
from recibo_restaurante.domain.producto import Producto
from recibo_restaurante.infrastructure.db.modelos import ProductoModelo


class RepositorioProductosSQLAlchemy(RepositorioProductos):
    def __init__(self, sesion: Session) -> None:
        self._sesion = sesion

    def listar(self) -> list[Producto]:
        modelos = self._sesion.query(ProductoModelo).all()
        return [self._a_entidad(modelo) for modelo in modelos]
    
    def listar_por_categoria(self, categoria_id: int) -> list[Producto]:
        modelos = (
            self._sesion.query(ProductoModelo)
            .filter(ProductoModelo.categoria_id == categoria_id)
            .all()
        )
        return [self._a_entidad(modelo) for modelo in modelos]
    
    def obtener_por_id(self, producto_id: int) -> Producto | None:
        modelo = self._sesion.get(ProductoModelo, producto_id)
        return self._a_entidad(modelo) if modelo else None
    
    def crear(self, producto: Producto) -> Producto:
        modelo = ProductoModelo(
            nombre=producto.nombre,
            precio=producto.precio,
            categoria_id=producto.categoria_id,
        )
        self._sesion.add(modelo)
        self._sesion.commit()
        self._sesion.refresh(modelo)
        return self._a_entidad(modelo)
    
    def actualizar(self, producto: Producto) -> Producto:
        modelo = self._sesion.get(ProductoModelo, producto.id)
        modelo.nombre = producto.nombre
        modelo.precio = producto.precio
        modelo.categoria_id = producto.categoria_id
        self._sesion.commit()
        self._sesion.refresh(modelo)
        return self._a_entidad(modelo)
    
    def eliminar(self, producto_id: int) -> None:
        modelo = self._sesion.get(ProductoModelo, producto_id)
        if modelo is not None:
            self._sesion.delete(modelo)
            self._sesion.commit()

    def _a_entidad(self, modelo: ProductoModelo) -> Producto:
        return Producto(
            id=modelo.id,
            nombre=modelo.nombre,
            precio=modelo.precio,
            categoria_id=modelo.categoria_id,
        )