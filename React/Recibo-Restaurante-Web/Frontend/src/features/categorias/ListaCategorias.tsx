import { useState } from "react"
import { crearCategoria, eliminarCategoria } from "../../api/categorias"
import { ApiError } from "../../api/client"
import { useDatos } from '../../context/DatosContext'

export function ListaCategorias() {
    const {categorias, cargando, recargarDatos} = useDatos()
    const [error, setError] = useState<string | null>(null)
    const [nombreNuevo, setNombreNuevo] = useState('')

    async function manejarCrear(evento: React.FormEvent) {
        evento.preventDefault()
        try {
            await crearCategoria(nombreNuevo)
            setNombreNuevo('')
            await recargarDatos()
            setError(null)
        } catch (error) {
            if (error instanceof ApiError) setError(error.message)
        }
    }

    async function manejarEliminar(categoriaId: number) {
        try {
            await eliminarCategoria(categoriaId)
            await recargarDatos()
        } catch (error) {
            if (error instanceof ApiError) setError(error.message)
        }
    }

    if (cargando) return <p className="text-slate-400">Cargando Categorías...</p>

    return (
        <div className="p-6 max-w-md mx-auto">
            <h2 className="text-2x1 font-bold text-white mb-4">Categorías</h2>

            {error && (
                <p className="bg-red-900 text-red-200 px-4 py-2 rounded mb-4">{error}</p>
            )}

            <form onSubmit={manejarCrear} className="flex gap-2 mb-6">
                <input
                    type="text"
                    value={nombreNuevo}
                    onChange={(evento) => setNombreNuevo(evento.target.value)}
                    placeholder="Nueva categoría"
                    className="flex-1 bg-slate-800 text-white px-3 py-2 rounded border border-slate-600"
                />
                <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded"
                >
                    Crear
                </button>
            </form>

            <ul className="space-y-2">
                {categorias.map((categoria) => (
                    <li
                        key={categoria.id}
                        className="flex justify-between items-center bg-slate-800 px-4 py-2 rounded"
                    >
                        <span className="text-white">{categoria.nombre}</span>
                        <button
                            onClick={() => manejarEliminar(categoria.id)}
                            className="text-red-400 hover:text-red-300"
                        >
                            Eliminar
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    )
}