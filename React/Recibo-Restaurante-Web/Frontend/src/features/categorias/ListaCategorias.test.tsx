import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import * as apiCategorias from '../../api/categorias'
import * as apiProductos from '../../api/productos'
import { DatosProvider } from '../../context/DatosContext'
import { ListaCategorias } from './ListaCategorias'

function renderConProvider() {
    return render(
        <DatosProvider>
            <ListaCategorias />
        </DatosProvider>,
    )
}

describe('ListaCategorias', () => {
    it('muestra las categorias que devuelve la API', async () => {
        vi.spyOn(apiCategorias, 'listarCategorias').mockResolvedValue([
            { id: 1, nombre: 'Bebidas' },
        ])
        vi.spyOn(apiProductos, 'listarProductos').mockResolvedValue([])

        renderConProvider()

        expect(await screen.findByText('Bebidas')).toBeInTheDocument()
    })

    it('crea una categoría nueva al enviar el formulario', async () => {
        vi.spyOn(apiCategorias, 'listarCategorias').mockResolvedValue([])
        vi.spyOn(apiProductos, 'listarProductos').mockResolvedValue([])
        const crearMock = vi.spyOn(apiCategorias, 'crearCategoria').mockResolvedValue({
            id: 2,
            nombre: 'Postres',
        })

        renderConProvider()

        const usuario = userEvent.setup()
        const input = await screen.findByPlaceholderText('Nueva categoría')
        await usuario.type(input, 'Postres')
        await usuario.click(screen.getByText('Crear'))

        await waitFor(() => {
            expect(crearMock).toHaveBeenCalledWith('Postres')
        })
    })

    it('muestra un mensaje de error si la API falla  al cargar', async () => {
        vi.spyOn(apiCategorias, 'listarCategorias').mockRejectedValue(new Error('falla de red'))
        vi.spyOn(apiProductos, 'listarProductos').mockResolvedValue([])

        renderConProvider()

        expect(await screen.findByText(/no se pudieron cargar/i)).toBeInTheDocument()
    })
})