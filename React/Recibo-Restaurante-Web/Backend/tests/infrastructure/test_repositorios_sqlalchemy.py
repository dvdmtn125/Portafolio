from recibo_restaurante.domain.categoria import Categoria
from recibo_restaurante.domain.producto import Producto
from recibo_restaurante.infrastructure.repositorios.repositorio_categorias_sqlalchemy import (
    RepositorioCategoriasSQLAlchemy,
)
from recibo_restaurante.infrastructure.repositorios.repositorio_productos_sqlalchemy import (
    RepositorioProductosSQLAlchemy,
)


def test_crear_y_listar_categoria(sesion_bd):
    repo = RepositorioCategoriasSQLAlchemy(sesion_bd)

    creada = repo.crear(Categoria(nombre='Bebidas'))

    assert creada.id is not None
    assert repo.listar() == [creada]


def test_obtener_categoria_por_id_inexistente_devuelve_none(sesion_bd):
    repo = RepositorioCategoriasSQLAlchemy(sesion_bd)
    assert repo.obtener_por_id(999) is None


def test_eliminar_categoria(sesion_bd):
    repo = RepositorioCategoriasSQLAlchemy(sesion_bd)
    creada = repo.crear(Categoria(nombre='Bebidas'))

    repo.eliminar(creada.id)

    assert repo.listar() == []


def test_crear_y_actualizar_producto(sesion_bd):
    repo_categorias = RepositorioCategoriasSQLAlchemy(sesion_bd)
    repo_productos = RepositorioProductosSQLAlchemy(sesion_bd)
    categoria = repo_categorias.crear(Categoria(nombre='Bebidas'))

    creado = repo_productos.crear(Producto(nombre='Limonada', precio=5000, categoria_id=categoria.id))
    actualizado = repo_productos.actualizar(
        Producto(id=creado.id, nombre='Limonada Grande', precio=7000, categoria_id=categoria.id)
    )

    assert actualizado.nombre == 'Limonada Grande'
    assert actualizado.precio == 7000


def test_listar_productos_por_categoria(sesion_bd):
    repo_categorias = RepositorioCategoriasSQLAlchemy(sesion_bd)
    repo_productos = RepositorioProductosSQLAlchemy(sesion_bd)
    bebidas = repo_categorias.crear(Categoria(nombre='Bebidas'))
    postres = repo_categorias.crear(Categoria(nombre='Postres'))
    repo_productos.crear(Producto(nombre='Limonada', precio=5000, categoria_id=bebidas.id))
    repo_productos.crear(Producto(nombre='Flan', precio=8000, categoria_id=postres.id))

    resultado = repo_productos.listar_por_categoria(bebidas.id)

    assert len(resultado) == 1
    assert resultado[0].nombre == 'Limonada'