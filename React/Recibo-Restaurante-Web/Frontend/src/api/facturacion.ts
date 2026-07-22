import { apiPost } from "./client"
import type {
    FacturaCalcularRequest,
    FacturaTotales,
    ReciboGenerarRequest,
    ReciboGenerarRespuesta,
} from './tipos'

export function calcularFactura(datos: FacturaCalcularRequest): Promise<FacturaTotales> {
    return apiPost<FacturaTotales>('/facturacion/calcular', datos)
}

export function generarRecibo(datos: ReciboGenerarRequest): Promise<ReciboGenerarRespuesta> {
    return apiPost<ReciboGenerarRespuesta>('/facturacion/recibo', datos)
}