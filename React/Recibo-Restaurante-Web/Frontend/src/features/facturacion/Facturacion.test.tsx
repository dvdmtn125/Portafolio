import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import * as apiCategorias from '../../api/categorias'
import * as apiFacturacion from '../../api/facturacion'
import * as apiProductos from '../../api/productos'
import { DatosProvider } from "../../context/DatosContext"
import { Facturacion } from "./Facturacion"

function renderConProvider() {
    return render(
        <DatosProvider>
            <Facturacion />
        </DatosProvider>,
    )
}
    
function mockearDatosBase() {
    vi.spyOn(apiCategorias, 'listarCategorias').mockResolvedValue([{ id: 1, nombre: 'Bebidas' }])
    vi.spyOn(apiProductos, 'listarProductos').mockResolvedValue([
        { id: 1, nombre: 'Limonada', precio: 5000, categoria_id: 1 },
    ])
}

describe('Facturacion', () => {
    it('agregar un ítem al pedido tras elegir categoría y producto', async () => {
        mockearDatosBase()
        renderConProvider()
        const usuario = userEvent.setup()

        const selects = await screen.findAllByRole('combobox')
        await usuario.selectOptions(selects[0], '1')
        await usuario.selectOptions(selects[1], '1')
        await usuario.click(screen.getByText('Agregar al pedido'))

        expect(await screen.findByText(/1x limonada/i)).toBeInTheDocument()
        expect(screen.getByText('Calcular factura')).toBeInTheDocument()
    })

    it('calcula la factura y muestra los totales', async () => {
        mockearDatosBase()
        vi.spyOn(apiFacturacion, 'calcularFactura').mockResolvedValue({
            bebidas: 5000,
            subtotal: 5000,
            iva: 950,
            total: 5950,
        })

        renderConProvider()
        const usuario = userEvent.setup()

        const selects = await screen.findAllByRole('combobox')
        await usuario.selectOptions(selects[0], '1')
        await usuario.selectOptions(selects[1], '1')
        await usuario.click(screen.getByText('Agregar al pedido'))
        await usuario.click(screen.getByText('Calcular factura'))

        expect(await screen.findByText(/total: \$5950/i)).toBeInTheDocument()
    })
})