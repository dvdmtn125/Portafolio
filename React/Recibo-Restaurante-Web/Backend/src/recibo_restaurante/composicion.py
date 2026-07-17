from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from recibo_restaurante.application.casos_uso.gestionar_categorias import (
    CrearCategoria,
    EliminarCategoria,
    ListarCategorias,
)
from recibo_restaurante.application.casos_uso.gestionar_productos import (
    ActualizarProducto,
    CrearProducto,
    EliminarProducto,
    ListarProductos,
)
from recibo_restaurante.application.casos_uso.calcular_factura import CalcularFactura
from recibo_restaurante.application.casos_uso.generar_recibo import GenerarRecibo
from recibo_restaurante.infrastructure.db.sesion import SesionLocal
from recibo_restaurante.infrastructure.repositorios.repositorio_categorias_sqlalchemy import (
    RepositorioCategoriasSQLAlchemy,
)
from recibo_restaurante.infrastructure.repositorios.repositorio_productos_sqlalchemy import (
    RepositorioProductosSQLAlchemy,
)


def obtener_sesion() -> Generator[Session, None, None]:
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()


def obtener_repositorio_categorias(
        sesion: Session = Depends(obtener_sesion),
    ) -> RepositorioCategoriasSQLAlchemy:
    return RepositorioCategoriasSQLAlchemy(sesion)


def obtener_repositorio_productos(
        sesion: Session = Depends(obtener_sesion),
    ) -> RepositorioProductosSQLAlchemy:
    return RepositorioProductosSQLAlchemy(sesion)


def obtener_listar_categorias(
        repo: RepositorioCategoriasSQLAlchemy = Depends(obtener_repositorio_categorias),
) -> ListarCategorias:
    return ListarCategorias(repo)


def obtener_crear_categoria(
        repo: RepositorioCategoriasSQLAlchemy = Depends(obtener_repositorio_categorias),
) -> CrearCategoria:
    return CrearCategoria(repo)


def obtener_eliminar_categoria(
        repo_categorias: RepositorioCategoriasSQLAlchemy = Depends(obtener_repositorio_categorias),
        repo_productos: RepositorioProductosSQLAlchemy = Depends(obtener_repositorio_productos),
) -> EliminarCategoria:
    return EliminarCategoria(repo_categorias, repo_productos)


def obtener_listar_productos(
        repo: RepositorioProductosSQLAlchemy = Depends(obtener_repositorio_productos),
) -> ListarProductos:
    return ListarProductos(repo)


def obtener_crear_producto(
        repo_productos: RepositorioProductosSQLAlchemy = Depends(obtener_repositorio_productos),
        repo_categorias: RepositorioCategoriasSQLAlchemy = Depends(obtener_repositorio_categorias),
) -> CrearProducto:
    return CrearProducto(repo_productos, repo_categorias)


def obtener_actualizar_producto(
        repo_producto: RepositorioProductosSQLAlchemy = Depends(obtener_repositorio_productos),
        repo_categorias: RepositorioCategoriasSQLAlchemy = Depends(obtener_repositorio_categorias),
) -> ActualizarProducto:
    return ActualizarProducto(repo_producto, repo_categorias)


def obtener_eliminar_producto(
        repo: RepositorioProductosSQLAlchemy = Depends(obtener_repositorio_productos),
) -> EliminarProducto:
    return EliminarProducto(repo)


def obtener_calcular_factura() -> CalcularFactura:
    return CalcularFactura()


def obtener_generar_recibo() -> GenerarRecibo:
    return GenerarRecibo()