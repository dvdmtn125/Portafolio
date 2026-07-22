export interface Categoria {
    id: number
    nombre: string
}

export interface Producto {
    id: number
    nombre: string
    precio: number
    categoria_id: number
}

export interface FacturaCalcularRequest {
    cantidades: Record<string, number[]>
    precios: Record<string,number[]>
}

export interface FacturaTotales {
    [categoria: string]: number
}

export interface ReciboItems {
    0: string // nombre
    1: number // cantidad
    2: number // precio unitario
}

export interface ReciboGenerarRequest {
    items: Record<string, [string, number, number][]>
    calculo: Record<string, number>
    numero_recibo?: string
}

export interface ReciboGenerarRespuesta {
    recibo: string
}