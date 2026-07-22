import { createContext, useContext, useEffect, useState, type ReactNode} from "react"
import { listarCategorias } from "../api/categorias"
import { listarProductos } from "../api/productos"
import type { Categoria, Producto } from "../api/tipos"

interface DatosContextValor {
    categorias: Categoria[]
    productos: Producto[]
    cargando: boolean
    recargarDatos: () => Promise<void>
}

const DatosContext = createContext<DatosContextValor | null>(null)

export function DatosProvider({ children }: { children: ReactNode }) {
    const [categorias, setCategorias] = useState<Categoria[]>([])
    const [productos,setProductos] = useState<Producto[]>([])
    const [cargando, setCargando] = useState(true)

    async function recargarDatos() {
        const [datosCategorias, datosProductos] = await Promise.all([
            listarCategorias(),
            listarProductos(),
        ])
        setCategorias(datosCategorias)
        setProductos(datosProductos)
    }

    useEffect(() => {
        recargarDatos().finally(() => setCargando(false))
    }, [])

    return (
        <DatosContext.Provider value={{ categorias, productos, cargando, recargarDatos }}>
            {children}
        </DatosContext.Provider>
    )
}

export function useDatos() {
    const contexto = useContext(DatosContext)
    if (!contexto) {
        throw new Error('useDatos debe usarse dentro de DatosProvider')
    }
    return contexto
}