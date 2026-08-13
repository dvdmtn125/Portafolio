import { AsistenciaProvider } from "./context/AsistenciaContext";
import { Dashboard } from "./pages/Dashboard";

function App() {
  return (
    <AsistenciaProvider>
      <Dashboard />
    </AsistenciaProvider>
  );
}

export default App;