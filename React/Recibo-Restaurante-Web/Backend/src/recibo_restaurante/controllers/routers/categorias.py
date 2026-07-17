from fastapi import APIRouter, Depends, HTTPException, status

from recibo_restaurante.application.casos_uso.gestionar_categorias import (
    CrearCategoria,
    EliminarCategoria,
    ListarCategorias,
)
from recibo_restaurante.application.excepciones import CategoriaConProductosAsociadosError
from recibo_restaurante.composicion import (
    obtener_crear_categoria,
    obtener_eliminar_categoria,
    obtener_listar_categorias,
)
from recibo_restaurante.controllers.schemas.categoria import CategoriaCrear, CategoriaRespuesta

router = APIRouter(prefix='/categorias', tags=['categorias'])


@router.get('/', response_model=list[CategoriaRespuesta])
def listar_categorias(caso_uso: ListarCategorias = Depends(obtener_listar_categorias)):
    return caso_uso.ejecutar()


@router.post('/', response_model=CategoriaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    datos: CategoriaCrear,
    caso_uso: CrearCategoria = Depends(obtener_crear_categoria),
):
    try:
        return caso_uso.ejecutar(datos.nombre)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    

@router.delete('/{categoria_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(
    categoria_id: int,
    caso_uso: EliminarCategoria = Depends(obtener_eliminar_categoria),
):
    try:
        caso_uso.ejecutar(categoria_id)
    except CategoriaConProductosAsociadosError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))