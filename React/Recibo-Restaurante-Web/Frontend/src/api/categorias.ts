import { apiDelete, apiGet, apiPost } from "./client"
import type { Categoria } from "./tipos"

export function listarCategorias(): Promise<Categoria[]> {
    return apiGet<Categoria[]>('/categorias/')
}

export function crearCategoria(nombre: string): Promise<Categoria> {
    return apiPost<Categoria>('/categorias/', { nombre })
}

export function eliminarCategoria(categoriaId: number): Promise<void> {
    return apiDelete(`/categorias/${categoriaId}`)
}