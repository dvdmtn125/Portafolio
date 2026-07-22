import { useState } from "react"
import { ApiError } from "../../api/client"
import { calcularFactura, generarRecibo } from "../../api/facturacion"
import { useDatos } from "../../context/DatosContext"
import type { FacturaTotales } from "../../api/tipos"

interface ItemPedido {
    productoId: number
    nombre: string
    categoriaNombre: string
    cantidad: number
    precioUnitario: number
}

export function Facturacion() {
    const {categorias, productos, cargando } = useDatos()
    const [error, setError] = useState<string | null>(null)

    const [categoriaId, setCategoriaId] = useState('')
    const [productoId, setProductoId] = useState('')
    const [cantidad, setCantidad] = useState('1')

    const [pedido, setPedido] = useState<ItemPedido[]>([])
    const [totales, setTotales] = useState<FacturaTotales | null>(null)
    const [reciboTexto, setReciboTexto] = useState<string | null>(null)

    const productosDeCategoria = productos.filter(
        (producto) => producto.categoria_id === Number(categoriaId),
    )

    function agregarAlPedido() {
        const producto = productos.find((p) => p.id === Number(productoId))
        const categoria = categorias.find((c) => c.id === Number(categoriaId))
        if (!producto || !categoria || Number(cantidad) <= 0) return

        setPedido([
            ...pedido,
            {
                productoId: producto.id,
                nombre: producto.nombre,
                categoriaNombre: categoria.nombre,
                cantidad: Number(cantidad),
                precioUnitario: producto.precio,
            },
        ])
        setProductoId('')
        setCantidad('1')
    }

    function quitarDelPedido(indice: number) {
        setPedido(pedido.filter((_, i) => i !== indice))
        setTotales(null)
        setReciboTexto(null)
    }

    async function manejarCalcular() {
        const cantidadesPorCategoria: Record<string, number[]> = {}
        const precioPorCategoria: Record<string, number[]> = {}

        for (const item of pedido) {
            const clave = item.categoriaNombre
            cantidadesPorCategoria[clave] = [...(cantidadesPorCategoria[clave] ?? []), item.cantidad]
            precioPorCategoria[clave] = [...(precioPorCategoria[clave] ?? []), item.precioUnitario]
        }

        try {
            const resultado = await calcularFactura({
                cantidades: cantidadesPorCategoria,
                precios: precioPorCategoria,
            })
            setTotales(resultado)
            setError(null)
        } catch (error) {
            if (error instanceof ApiError) setError(error.message)
        }
    }

    async function manejarGenerarRecibo() {
        if (!totales) return

        const itemsPorCategoria: Record<string, [string, number, number][]> = {}
        for (const item of pedido) {
            const clave = item.categoriaNombre
            const tupla: [string, number, number] = [item.nombre, item.cantidad, item.precioUnitario]
            itemsPorCategoria[clave] = [...(itemsPorCategoria[clave] ?? []), tupla]
        }
        
        try {
            const resultado = await generarRecibo({ items: itemsPorCategoria, calculo: totales })
            setReciboTexto(resultado.recibo)
        } catch (error) {
            if (error instanceof ApiError) setError(error.message)
        }
    }

    function nuevoPedido() {
        setPedido([])
        setTotales(null)
        setReciboTexto(null)
    }

    if (cargando) return <p className="text-slate-400">Cargando...</p>

    return(
        <div className="p-6 max-w-lg mx-auto">
            <h2 className="text-2xl font-bold text-white mb-4">Facturación</h2>

            {error && <p className="bg-red-900 text-red-200 px-4 py-2 rounded mb-4">{error}</p>}

            <div className="flex flex-col gap-2 mb-4">
                <select
                    value={categoriaId}
                    onChange={(evento) => {
                        setCategoriaId(evento.target.value)
                        setProductoId('')
                    }}
                    className="bg-slate-800 text-white px-3 py-2 rounded border border-slate-600">
                        <option value="">Seleccioná una categoría</option>
                        {categorias.map((categoria) => (
                            <option key={categoria.id} value={categoria.id}>
                                {categoria.nombre}
                            </option>
                        ))}
                </select>

                <select
                    value={productoId}
                    onChange={(evento) => setProductoId(evento.target.value)}
                    disabled={!categoriaId}
                    className="bg-slate-800 text-white px-3 py-2 rounded border border-slate-600 disabled:opacity-50"
                >
                    <option value="">Seleccioná un producto</option>
                    {productosDeCategoria.map((producto) => (
                        <option key={producto.id} value={producto.id}>
                            {producto.nombre} - ${producto.precio}
                        </option>
                    ))}
                </select>

                <input
                    type="number"
                    min="1"
                    value={cantidad}
                    onChange={(evento) => setCantidad(evento.target.value)}
                    className="bg-slate-800 text-white px-3 py-2 rounded border border-slate-600" />
                <button
                    onClick={agregarAlPedido}
                    disabled={!productoId}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50">
                    Agregar al pedido
                </button>
            </div>
            {pedido.length > 0 && (
                <div className="mb-4">
                    <h3 className="text-lg font-semibold text-white mb-2">Pedido actual</h3>
                    <ul className="space-y-2">
                        {pedido.map((item, indice) => (
                            <li
                                key={indice}
                                className="flex justify-between items-center gap-4 bg-slate-800 px-4 py-2 rounded"
                            >
                                <span className="text-white">
                                    {item.cantidad}x {item.nombre} - ${item.cantidad * item.precioUnitario}
                                </span>
                                <button 
                                    onClick={() => quitarDelPedido(indice)}
                                    className="text-red-400 hover:text-red-300 flex-shrink-0"
                                >
                                    Quitar
                                </button>
                            </li>
                        ))}
                    </ul>
                    <button
                        onClick={manejarCalcular}
                        className="mt-4 bg-green-600 hover:bg-green-500 text-white px-4 py-2 rounded w-full"
                    >
                        Calcular factura
                    </button>
                </div>
            )}

            {totales && (
                <div className="mb-4 bg-slate-800 p-4 rounded text-white">
                    <p>Subtotal: ${totales.subtotal}</p>
                    <p>IVA: ${totales.iva}</p>
                    <p className="font-bold">Total: ${totales.total}</p>

                    <button
                        onClick={manejarGenerarRecibo}
                        className="mt-4 bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded w-full"
                    >
                        Generar recibo
                    </button>
                </div>
            )}

            {reciboTexto && (
                <div className="mb-4">
                    <pre className="bg-slate-950 text-green-400 p-4 rounded whitespace-pre-wrap text-sm">
                        {reciboTexto}
                    </pre>
                    <button
                        onClick={nuevoPedido}
                        className="mt-4 bg-slate-600 hover:bg-slate-500 text-white px-4 py-2 rounded w-full"
                    >
                        Nuevo pedido
                    </button>
                </div>
            )}
        </div>
    )
}