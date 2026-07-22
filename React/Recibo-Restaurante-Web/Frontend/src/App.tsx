import { DatosProvider } from "./context/DatosContext"
import { Facturacion } from "./features/facturacion/Facturacion"
import { ListaCategorias } from "./features/categorias/ListaCategorias"
import { ListaProductos } from "./features/productos/ListaProductos"

function App() {
  return (
    <DatosProvider>
      <div className="min-h-screen bg-slate-900 flex flex-col md:flex-row gap-4">
        <ListaCategorias />
        <ListaProductos />
        <Facturacion />
      </div>
    </DatosProvider>
  )
}

export default App