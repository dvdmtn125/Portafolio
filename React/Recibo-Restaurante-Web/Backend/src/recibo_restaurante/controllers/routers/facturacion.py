from fastapi import APIRouter, Depends, HTTPException, status

from recibo_restaurante.application.casos_uso.calcular_factura import CalcularFactura
from recibo_restaurante.application.casos_uso.generar_recibo import GenerarRecibo
from recibo_restaurante.composicion import obtener_calcular_factura, obtener_generar_recibo
from recibo_restaurante.controllers.schemas.factura import FacturaCalcularRequest
from recibo_restaurante.controllers.schemas.recibo import ReciboGenerarRequest, RecibogenerarRespuesta

router = APIRouter(prefix='/facturacion', tags=['facturacion'])


@router.post('/calcular', response_model=dict[str, float])
def calcular_factura(
    datos: FacturaCalcularRequest,
    caso_uso: CalcularFactura = Depends(obtener_calcular_factura)
):
    try:
        return caso_uso.ejecutar(datos.cantidades, datos.precios)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    

@router.post('/recibo', response_model=RecibogenerarRespuesta)
def generar_recibo(
    datos: ReciboGenerarRequest,
    caso_uso: GenerarRecibo = Depends(obtener_generar_recibo),
):
    texto = caso_uso.ejecutar(datos.items, datos.calculo, datos.numero_recibo)
    return RecibogenerarRespuesta(recibo=texto)