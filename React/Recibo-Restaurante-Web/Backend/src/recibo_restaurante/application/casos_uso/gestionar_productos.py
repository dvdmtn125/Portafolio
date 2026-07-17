from recibo_restaurante.application.interfaces.repositorio_categorias import RepositorioCategorias
from recibo_restaurante.application.interfaces.repositorio_productos import RepositorioProductos
from recibo_restaurante.domain.producto import Producto


class ListarProductos:
    def __init__(self, repositorio_productos: RepositorioProductos) -> None:
        self._repositorio_productos = repositorio_productos

    def ejecutar(self) -> list[Producto]:
        return self._repositorio_productos.listar()
    

class CrearProducto:
    def __init__(
            self,
            repositorio_productos: RepositorioProductos,
            repositorio_categorias: RepositorioCategorias,
    ) -> None:
        self._repositorio_productos = repositorio_productos
        self._repositorio_categorias = repositorio_categorias

    def ejecutar(self, nombre: str, precio: float, categoria_id: int) -> Producto:
        categoria = self._repositorio_categorias.obtener_por_id(categoria_id)
        if categoria is None:
            raise ValueError(f'La categoría {categoria_id} no existe.')
        
        producto = Producto(nombre=nombre, precio=precio, categoria_id=categoria_id)
        return self._repositorio_productos.crear(producto)
    

class ActualizarProducto:
    def __init__(
            self,
            repositorio_productos: RepositorioProductos,
            repositorio_categorias: RepositorioCategorias,
    ) -> None:
        self._repositorio_productos = repositorio_productos
        self._repositorio_categorias = repositorio_categorias

    def ejecutar(self, producto_id: int, nombre: str, precio: float, categoria_id: int) -> Producto:
        if self._repositorio_categorias.obtener_por_id(categoria_id) is None:
            raise ValueError(f'La categoría {categoria_id} no existe.')
        
        producto_existente = self._repositorio_productos.obtener_por_id(producto_id)
        if producto_existente is None:
            raise ValueError(f'El producto {producto_id} no existe.')
        
        producto = Producto(id=producto_id, nombre=nombre, precio=precio, categoria_id=categoria_id)
        return self._repositorio_productos.actualizar(producto)
    

class EliminarProducto:
    def __init__(self, repositorio_productos: RepositorioProductos) -> None:
        self._repositorio_productos = repositorio_productos

    def ejecutar(self, producto_id: int) -> None:
        self._repositorio_productos.eliminar(producto_id)