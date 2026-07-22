import { useState } from "react"
import { ApiError } from "../../api/client"
import { actualizarProducto, crearProducto, eliminarProducto } from "../../api/productos"
import { useDatos } from "../../context/DatosContext"
import type { Producto } from "../../api/tipos"

export function ListaProductos() {
    const { categorias, productos, cargando, recargarDatos } = useDatos()
    const [error, setError] = useState<string | null>(null)

    const [nombre, setNombre] = useState('')
    const [precio, setPrecio] = useState('')
    const [categoriaId, setCategoriaId] = useState('')
    const [productoEditando, setProductoEditando] = useState<Producto | null>(null)

    function nombreDeCategoria(categoriaId: number): string {
        return categorias.find((c) => c.id == categoriaId)?.nombre ?? 'Desconocida'
    }

    function iniciarEdicion(producto: Producto) {
        setProductoEditando(producto)
        setNombre(producto.nombre)
        setPrecio(String(producto.precio))
        setCategoriaId(String(producto.categoria_id))
    }

    function cancelarEdicion() {
        setProductoEditando(null)
        setNombre('')
        setPrecio('')
        setCategoriaId('')
    }

    async function manejarSubmit(evento: React.FormEvent) {
        evento.preventDefault()
        const datos = {
            nombre,
            precio: Number(precio),
            categoria_id: Number(categoriaId), 
        }

        try {
            if (productoEditando) {
                await actualizarProducto(productoEditando.id, datos)
            } else {
                await crearProducto(datos)
            }
            cancelarEdicion()
            await recargarDatos()
            setError(null)
        } catch (error) {
            if (error instanceof ApiError){
                setError(error.message)
            }
        }
    }

    async function manejarEliminar(productoId: number) {
        try {
            await eliminarProducto(productoId)
            if (productoEditando?.id == productoId) cancelarEdicion()
            await recargarDatos()
            setError(null)
        } catch (error) {
            if (error instanceof ApiError) {
                setError(error.message)
            }
        }
    }

    if (cargando) return <p className="text-slate-400">Cargando productos...</p>

    const hayCategorias = categorias.length > 0

    return (
        <div className="p-6 max-w-md mx-auto">
            <h2 className="text_2xl font-bold text-white mb-4">Productos</h2>

            {error && (
                <p className="bg-red-900 text-red-200 px-4 py-2 rounded mb-4">{error}</p>
            )}

            {!hayCategorias && (
                <p className="bg-yellow-900 text-yellow-200 px-4 py-2 rounded mb-4">
                    Creá una categoría primero para poder agregar productos.
                </p>
            )}

            {productoEditando && (
                <p className="bg-blue-900 text-blue-200 px-4 py-2 rounded mb-2 text-sm">
                    Editando: {productoEditando.nombre}
                </p>
            )}

            <form onSubmit={manejarSubmit} className="flex flex-col gap-2 mb-6">
                <input
                    type="text"
                    value={nombre}
                    onChange={(evento) => setNombre(evento.target.value)}
                    placeholder="Nombre del producto"
                    disabled={!hayCategorias}
                    className="bg-slate-800 text-white px-3 py-2 rounded border border-slate-600 disabled:opacity-50" 
                />
                <input
                    type="number"
                    value={precio}
                    onChange={(evento) => setPrecio(evento.target.value)}
                    placeholder="Precio"
                    disabled={!hayCategorias}
                    className="bg-slate-800 text-white px-3 py-2 rounded border border-slate-600 disabled:opacity-50" 
                />
                <select
                    value={categoriaId}
                    onChange={(evento) => setCategoriaId(evento.target.value)}
                    disabled={!hayCategorias}
                    className="bg-slate-800 text-white px-3 py-2 rounded border border-slate-600 disabled:opacity-50">
                        <option value="">Seleccioná una categoría</option>
                        {categorias.map((categoria) => (
                            <option key={categoria.id} value={categoria.id}>
                                {categoria.nombre}
                            </option>
                        ))}
                </select>
                <div className="flex gap-2">
                    <button
                        type="submit"
                        disabled={!hayCategorias || !categoriaId}
                        className="flex-1 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {productoEditando ? 'Guardar cambios' : 'Crear producto'}
                    </button>
                    {productoEditando && (
                        <button
                            type="button"
                            onClick={cancelarEdicion}
                            className="bg-slate-600 hover:bg-slate-500 text-white px-4 py-2 rounded">
                                Cancelar
                            </button>
                    )}
                </div>
            </form>

            <ul className="space-y-2">
                {productos.map((producto) => (
                    <li
                        key={producto.id}
                        className="flex justify-between items-center gap-4 bg-slate-800 px-4 py-2 rounded"
                    >
                        <div>
                            <span className="text-white">{producto.nombre}</span>
                            <span className="text-slate-400 text-sm ml-2">
                                ({nombreDeCategoria(producto.categoria_id)}) - ${producto.precio}
                            </span>
                        </div>
                        <div className="flex gap-3 flex-shrink-0">
                            <button
                                onClick={() => iniciarEdicion(producto)}
                                className="tetx-blue-400 hover:text-blue-300"
                            >
                                Editar
                            </button>
                            <button
                                onClick={() => manejarEliminar(producto.id)}
                                className="text-red-400 hover:text-red-300 flex-shrink-0"
                            >
                                Eliminar
                            </button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    )
}