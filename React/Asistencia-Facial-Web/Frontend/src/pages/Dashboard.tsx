import { AsistenciaFeed } from "../components/AsistenciaFeed";
import { RegistroPersonaForm } from "../components/RegistroPersonaForm";
import { WebcamCapture } from "../components/WebcamCapture";

export function Dashboard() {
    return (
        <div className="mx-auto flex max-w-4xl flex-col gap-8 p-6">
            <header>
                <h1 className="text-xl font-semibold">Asistencia facial</h1>
                <p className="text-sm text-neutral-500">
                    Dashboard de control de asistencia mediante reconocimiento facial en vivo.
                </p>
            </header>

            <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
                <WebcamCapture />
                <AsistenciaFeed />
            </div>

            <div className="border-t border-neutral-200 pt-8">
                <RegistroPersonaForm />
            </div>
        </div>
    );
}