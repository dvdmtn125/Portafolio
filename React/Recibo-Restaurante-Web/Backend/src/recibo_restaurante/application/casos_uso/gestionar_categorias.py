from recibo_restaurante.application.excepciones import CategoriaConProductosAsociadosError
from recibo_restaurante.application.interfaces.repositorio_categorias import RepositorioCategorias
from recibo_restaurante.application.interfaces.repositorio_productos import RepositorioProductos
from recibo_restaurante.domain.categoria import Categoria


class ListarCategorias:
    def __init__(self, repositorio_categorias: RepositorioCategorias) -> None:
        self._repositorio_categorias = repositorio_categorias

    def ejecutar(self) -> list[Categoria]:
        return self._repositorio_categorias.listar()
    

class CrearCategoria:
    def __init__(self, repositorio_categorias: RepositorioCategorias) -> None:
        self._repositorio_categorias = repositorio_categorias

    def ejecutar(self, nombre: str) -> Categoria:
        categoria = Categoria(nombre=nombre)
        return self._repositorio_categorias.crear(categoria)
    

class EliminarCategoria:
    def __init__(
            self,
            repositorio_categorias: RepositorioCategorias,
            repositorio_productos: RepositorioProductos,
    ) -> None:
        self._repositorio_categorias = repositorio_categorias
        self._repositorio_productos = repositorio_productos

    def ejecutar(self, categoria_id: int) -> None:
        productos_asociados = self._repositorio_productos.listar_por_categoria(categoria_id)
        if productos_asociados:
            raise CategoriaConProductosAsociadosError(
                categoria_id=categoria_id,
                cantidad_productos=len(productos_asociados),
            )
        self._repositorio_categorias.eliminar(categoria_id)