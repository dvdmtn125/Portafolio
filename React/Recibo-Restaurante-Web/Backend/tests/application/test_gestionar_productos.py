import pytest

from recibo_restaurante.application.casos_uso.gestionar_productos import (
    ActualizarProducto,
    CrearProducto,
    EliminarProducto,
    ListarProductos,
)
from recibo_restaurante.domain.categoria import Categoria
from recibo_restaurante.domain.producto import Producto


def test_listar_productos_devuelve_lo_que_da_el_repositorio(mocker):
    repo_falso = mocker.Mock()
    repo_falso.listar.return_value = [Producto(nombre='Limonada', precio=5000, categoria_id=1)]

    caso_uso = ListarProductos(repo_falso)
    resultado = caso_uso.ejecutar()

    assert len(resultado) == 1
    repo_falso.listar.assert_called_once()


def test_crear_producto_con_categoria_existente_lo_crea(mocker):
    repo_productos = mocker.Mock()
    repo_categorias = mocker.Mock()
    repo_categorias.obtener_por_id.return_value = Categoria(nombre='Bebidas', id=1)
    repo_productos.crear.return_value = Producto(nombre='Limonada', precio=5000, categoria_id=1, id=1)

    caso_uso = CrearProducto(repo_productos, repo_categorias)
    resultado = caso_uso.ejecutar(nombre='Limonada', precio=5000, categoria_id=1)

    assert resultado.id == 1
    repo_categorias.obtener_por_id.assert_called_once_with(1)
    repo_productos.crear.assert_called_once_with(Producto(nombre='Limonada', precio=5000, categoria_id=1))


def test_crear_producto_con_categoria_inexistente_no_llega_al_repositorio_de_productos(mocker):
    repo_productos = mocker.Mock()
    repo_categorias = mocker.Mock()
    repo_categorias.obtener_por_id.return_value = None

    caso_uso = CrearProducto(repo_productos, repo_categorias)
    with pytest.raises(ValueError):
        caso_uso.ejecutar(nombre='Limonada', precio=5000, categoria_id=999)

    repo_productos.crear.assert_not_called()


def test_actualizar_producto_inexistente_lanza_error(mocker):
    repo_productos = mocker.Mock()
    repo_categorias = mocker.Mock()
    repo_categorias.obtener_por_id.return_value = Categoria(nombre='Bebidas', id=1)
    repo_productos.obtener_por_id.return_value = None

    caso_uso = ActualizarProducto(repo_productos, repo_categorias)
    with pytest.raises(ValueError):
        caso_uso.ejecutar(producto_id=999, nombre='Limonada', precio=5000, categoria_id=1)

    repo_productos.actualizar.assert_not_called()


def test_eliminar_producto_llama_al_repositorio(mocker):
    repo_falso = mocker.Mock()

    caso_uso = EliminarProducto(repo_falso)
    caso_uso.ejecutar(producto_id=1)

    repo_falso.eliminar.assert_called_once_with(1)