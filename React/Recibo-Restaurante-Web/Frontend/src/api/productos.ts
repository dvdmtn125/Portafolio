import { apiDelete, apiGet, apiPost, apiPut } from "./client"
import type { Producto } from './tipos'

interface ProductoDatos {
    nombre:string
    precio: number
    categoria_id: number
}

export function listarProductos(): Promise<Producto[]> {
    return apiGet<Producto[]>('/productos/')
}

export function crearProducto(datos: ProductoDatos): Promise<Producto> {
    return apiPost<Producto>('/productos/', datos)
}

export function actualizarProducto(productoId: number, datos: ProductoDatos): Promise<Producto> {
    return apiPut<Producto>(`/productos/${productoId}`, datos)
}

export function eliminarProducto(productoId: number): Promise<void> {
    return apiDelete(`/productos/${productoId}`)
}