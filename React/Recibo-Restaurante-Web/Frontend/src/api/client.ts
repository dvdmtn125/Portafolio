const BASE_URL = 'http://localhost:8000'

export class ApiError extends Error {
    status: number
    constructor(
        message: string, status: number) {
        super(message)
        this.status = status
        this.name = 'ApiError'
    }
}

async function manejarRespuesta<T>(respuesta: Response): Promise<T> {
    if (!respuesta.ok) {
        const cuerpo = await respuesta.json().catch(() => null)
        const mensaje = cuerpo?.detail ?? `Error ${respuesta.status}`
        throw new ApiError(mensaje, respuesta.status)
    }
    if (respuesta.status === 204) {
        return undefined as T
    }
    return respuesta.json()
}

export async function apiGet<T>(ruta: string): Promise<T> {
    const respuesta = await fetch(`${BASE_URL}${ruta}`)
    return manejarRespuesta<T>(respuesta)
}

export async function apiPost<T>(ruta: string, datos: unknown): Promise<T> {
    const respuesta = await fetch(`${BASE_URL}${ruta}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos),
    })
    return manejarRespuesta<T>(respuesta)
}

export async function apiPut<T>(ruta: string, datos: unknown): Promise<T> {
    const respuesta = await fetch(`${BASE_URL}${ruta}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos),
    })
    return manejarRespuesta<T>(respuesta)
}

export async function apiDelete(ruta: string): Promise<void> {
    const respuesta = await fetch(`${BASE_URL}${ruta}`, { method: 'DELETE' })
    await manejarRespuesta<void>(respuesta)
}