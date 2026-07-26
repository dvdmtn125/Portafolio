import { describe, expect, it, vi } from "vitest"
import { ApiError, apiDelete, apiGet, apiPost } from "./client"

function mockearFetch(respuesta: { ok: boolean; status: number; json: () => Promise<unknown> }) {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(respuesta))
}

describe('apiGet', () => {
    it('devuelve los datos cuando la respuesta es exitosa', async () => {
        mockearFetch({ok: true, status: 200, json: async () => [{ id: 1, nombre: 'Bebidas'}] })

        const resultado = await apiGet('/categorias/')

        expect(resultado).toEqual([{ id:1, nombre: 'Bebidas' }])
    })

    it('lanza ApiError con el mensaje del backend cuando la respuesta falla', async () => {
        mockearFetch({ ok: false, status: 400, json: async () => ({ detail: 'Nombre inválido' }) })

        await expect(apiGet('/categorias/')).rejects.toThrow('Nombre inválido')
    })

    it('el ApiError lanzado tiene el status code correcto', async () => {
        mockearFetch({ ok: false, status: 409, json: async () => ({ detail: 'Conflito' }) })

        try {
            await apiGet('/categoria/1')
            throw new Error('Se esperaba que lanzara')
        } catch (error) {
            expect(error).toBeInstanceOf(ApiError)
            expect((error as ApiError).status).toBe(409)
        }
    })
})

describe('apiDelete', () => {
    it('no lanza error con una respuesta 204 sin cuerpo', async () => {
        mockearFetch({ ok: true, status: 204, json: async () => { throw new Error('no debería llamarse') } })

        await expect(apiDelete('/productos/1')).resolves.toBeUndefined()
    })
})

describe('apiPost', () => {
    it('envia el body como JSON y devuelve la respuesta', async () => {
        const fetchMock = vi.fn().mockResolvedValue({
            ok: true,
            status: 201,
            json: async () => ({ id:1, nombre: 'Bebidas' }),
        })
        vi.stubGlobal('fetch', fetchMock)

        await apiPost('/categorias/', { nombre: 'Bebidas' })

        expect(fetchMock).toHaveBeenCalledWith(
            expect.stringContaining('/categorias/'),
            expect.objectContaining({
                method: 'POST',
                body: JSON.stringify({ nombre: 'Bebidas' }),
            }),
        )
    })
})