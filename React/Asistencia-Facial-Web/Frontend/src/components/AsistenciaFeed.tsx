import { useEffect } from "react";

import { useAsistencia } from "../context/AsistenciaContext";

function formatearHora(fecha: Date): string {
    return fecha.toLocaleTimeString("es-CO", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    });
}

export function AsistenciaFeed() {
    const { ultimosEventos, registroDeHoy, errorConexion, refrescarRegistro } =
    useAsistencia();

    useEffect(() => {
        void refrescarRegistro();
    }, [refrescarRegistro]);

    return (
        <div className="flex flex-col-gap-6">
            {errorConexion && (
                <div className="rounded-md border border-red-300 bg-red-50 px-4 py-2 text-sm text-red-700">
                    {errorConexion}
                </div>
            )}

            <section>
                <h2 className="mb-2 tetx-sm font-medium text-neutral-500">
                    Feed en vivo
                </h2>
                {ultimosEventos.length === 0 ? (
                    <p className="text-sm tetx-neutral-400">
                        Aún no hay reconociminetos en esta sesión.
                    </p>
                ) : (
                    <ul className="flex flex-col gap-1">
                        {ultimosEventos.map((evento) => (
                            <li
                                key={evento.id}
                                className="flex items-center justify-between rounded-md border border-neutral-200 px-3 py-2 text-sm"
                            >

                                <span>
                                    {evento.resultado.reconocido
                                        ? evento.resultado.nombre
                                        : "No reconocido"}
                                </span>
                                <span className="text-neutral-400">
                                    {formatearHora(evento.timestamp)}
                                </span>
                            </li>
                        ))}
                    </ul>
                )}
            </section>

            <section>
                <h2 className="mb-2 text-sm font-medium text-neutral-500">
                    Asistencias de hoy
                </h2>
                {registroDeHoy.length === 0 ? (
                    <p className="text-sm text-neutral-400">
                        Nadie ha marcado asistencia todavia.
                    </p>
                ) : (
                    <ul className="flex flex-col gap-1">
                        {registroDeHoy.map((registro) => (
                            <li
                                key={registro.persona_id}
                                className="flex items-center justify-between rounded-md border border-neutral-200 px-3 py-2 text-sm"
                            >
                                <span>{registro.nombre}</span>
                            </li>
                        ))}
                    </ul>
                )}
            </section>
        </div>
    );
}