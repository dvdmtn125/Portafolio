import pytest

from recibo_restaurante.application.casos_uso.gestionar_categorias import (
    CrearCategoria,
    EliminarCategoria,
    ListarCategorias,
)
from recibo_restaurante.application.excepciones import CategoriaConProductosAsociadosError
from recibo_restaurante.domain.categoria import Categoria
from recibo_restaurante.domain.producto import Producto


def test_listar_categorias_devuelve_lo_que_da_el_repositorio(mocker):
    repo_falso = mocker.Mock()
    repo_falso.listar.return_value = [Categoria(nombre='Bebidas', id=1)]

    caso_uso = ListarCategorias(repo_falso)
    resultado = caso_uso.ejecutar()

    assert resultado == [Categoria(nombre='Bebidas', id=1)]
    repo_falso.listar.assert_called_once_with()


def test_crear_categoria_llama_al_repositorio_con_la_entidad_correcta(mocker):
    repo_falso = mocker.Mock()
    repo_falso.crear.return_value = Categoria(nombre='Bebidas', id=1)

    caso_uso = CrearCategoria(repo_falso)
    resultado = caso_uso.ejecutar('Bebidas')

    assert resultado.id == 1
    repo_falso.crear.assert_called_once_with(Categoria(nombre='Bebidas'))


def test_crear_categoria_nombre_invalido_no_llega_al_repositorio(mocker):
    repo_falso = mocker.Mock()

    caso_uso = CrearCategoria(repo_falso)
    with pytest.raises(ValueError):
        caso_uso.ejecutar('')

    repo_falso.crear.assert_not_called()


def test_eliminar_categoria_sin_productos_la_elimina(mocker):
    repo_categorias = mocker.Mock()
    repo_productos = mocker.Mock()
    repo_productos.listar_por_categoria.return_value = []

    caso_uso = EliminarCategoria(repo_categorias, repo_productos)
    caso_uso.ejecutar(categoria_id=1)

    repo_categorias.eliminar.assert_called_once_with(1)


def test_eliminar_categoria_con_productos_lanza_error_y_no_eliminar(mocker):
    repo_categorias = mocker.Mock()
    repo_productos = mocker.Mock()
    repo_productos.listar_por_categoria.return_value = [
        Producto(nombre='Limonada', precio=5000, categoria_id=1, id=1)
    ]

    caso_uso = EliminarCategoria(repo_categorias, repo_productos)
    with pytest.raises(CategoriaConProductosAsociadosError):
        caso_uso.ejecutar(categoria_id=1)

    repo_categorias.eliminar.assert_not_called()