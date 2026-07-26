import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import * as apiCategorias from '../../api/categorias'
import * as apiProductos from '../../api/productos'
import { DatosProvider } from "../../context/DatosContext"
import { ListaProductos } from "./ListaProductos"

function renderConProvider() {
    return render(
        <DatosProvider>
            <ListaProductos />
        </DatosProvider>
    )
}

describe('ListaProductos', () => {
    it('muestra productos con el nombre de la categoría', async () => {
        vi.spyOn(apiCategorias, 'listarCategorias').mockResolvedValue([{ id: 1, nombre: 'Bebidas' }])
        vi.spyOn(apiProductos, 'listarProductos').mockResolvedValue([
            { id: 1, nombre: 'Limonada', precio: 5000, categoria_id: 1 },
        ])

        renderConProvider()

        expect(await screen.findByText('Limonada')).toBeInTheDocument()
        expect(await screen.findByText(/\(Bebidas\)/)).toBeInTheDocument()
    })

    it('deshabilita el formulario si no hay categorías', async () => {
        vi.spyOn(apiCategorias, 'listarCategorias').mockResolvedValue([])
        vi.spyOn(apiProductos, 'listarProductos').mockResolvedValue([])

        renderConProvider()

        expect(await screen.findByText(/creá una categoría primero/i)).toBeInTheDocument()
        expect(screen.getByPlaceholderText('Nombre del producto')).toBeDisabled()
    })

    it('crea un producto con los datos del formulario', async () => {
        vi.spyOn(apiCategorias, 'listarCategorias').mockResolvedValue([{ id: 1, nombre: 'Bebidas' }])
        vi.spyOn(apiProductos, 'listarProductos').mockResolvedValue([])
        const crearMock = vi.spyOn(apiProductos, 'crearProducto').mockResolvedValue({
            id: 1,
            nombre: 'Limonada',
            precio: 5000,
            categoria_id: 1,
        })

        renderConProvider()
        const usuario = userEvent.setup()

        await usuario.type(await screen.findByPlaceholderText('Nombre del producto'), 'Limonada')
        await usuario.type(screen.getByPlaceholderText('Precio'), '5000')
        await usuario.selectOptions(screen.getByRole('combobox'), '1')
        await usuario.click(screen.getByText('Crear producto'))

        expect(crearMock).toHaveBeenCalledWith({ nombre: 'Limonada', precio: 5000, categoria_id: 1 })
    })

    it('entra en modo edición al hacer clic en Editar', async () => {
        vi.spyOn(apiCategorias, 'listarCategorias').mockResolvedValue([{ id: 1, nombre: 'Bebidas' }])
        vi.spyOn(apiProductos, 'listarProductos').mockResolvedValue([
            { id: 1, nombre: 'Limonada', precio: 5000, categoria_id: 1 },
        ])

        renderConProvider()
        const usuario = userEvent.setup()

        await usuario.click(await screen.findByText('Editar'))

        expect(screen.getByText(/editando: limonada/i)).toBeInTheDocument()
        expect(screen.getByText('Guardar cambios')).toBeInTheDocument()
        expect(screen.getByPlaceholderText('Nombre del producto')).toHaveValue('Limonada')
    })
})