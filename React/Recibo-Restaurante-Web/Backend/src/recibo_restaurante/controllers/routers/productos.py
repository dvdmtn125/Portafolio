from fastapi import APIRouter, Depends, HTTPException, status

from recibo_restaurante.application.casos_uso.gestionar_productos import (
    ActualizarProducto,
    CrearProducto,
    EliminarProducto,
    ListarProductos,
)
from recibo_restaurante.composicion import (
    obtener_actualizar_producto,
    obtener_crear_producto,
    obtener_eliminar_producto,
    obtener_listar_productos,
)
from recibo_restaurante.controllers.schemas.producto import (
    ProductoActualizar,
    ProductoCrear,
    ProductoRespuesta,
)

router = APIRouter(prefix='/productos', tags=['productos'])


@router.get('/', response_model=list[ProductoRespuesta])
def listar_productos(caso_uso: ListarProductos = Depends(obtener_listar_productos)):
    return caso_uso.ejecutar()


@router.post('/', response_model=ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_producto(
    datos: ProductoCrear,
    caso_uso: CrearProducto = Depends(obtener_crear_producto),
):
    try:
        return caso_uso.ejecutar(datos.nombre, datos.precio, datos.categoria_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    

@router.put('/{producto_id}', response_model=ProductoRespuesta)
def actualizar_producto(
    producto_id: int,
    datos: ProductoActualizar,
    caso_uso: ActualizarProducto = Depends(obtener_actualizar_producto),
):
    try:
        return caso_uso.ejecutar(producto_id, datos.nombre, datos.precio, datos.categoria_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    

@router.delete('/{producto_id}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: int,
    caso_uso: EliminarProducto = Depends(obtener_eliminar_producto),
):
    caso_uso.ejecutar(producto_id)