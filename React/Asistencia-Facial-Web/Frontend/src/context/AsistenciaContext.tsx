import {
    createContext,
    useCallback,
    useContext,
    useState,
    type ReactNode,
} from "react";

import { 
    listarAsistencias,
    reconocerFrame,
    ErrorApiAsistencia,
} from "../services/asistenciaApi";
import type {
    ReconocimientoSalida,
    RegistroAsistenciaSalida,
} from "../types/asistencia";

interface EventoReconocimiento {
    id: string;
    resultado: ReconocimientoSalida;
    timestamp: Date;
}

interface AsistenciaContextvalue {
    registroDeHoy:RegistroAsistenciaSalida[];
    ultimosEventos: EventoReconocimiento[];
    errorConexion: string | null;
    procesarFrame: (imagenBase64: string) => Promise<void>;
    refrescarRegistro: () => Promise<void>;
}

const AsistenciaContext = createContext<AsistenciaContextvalue | undefined>(undefined);

const MAX_EVENTOS_EN_FEED = 20;

export function AsistenciaProvider({ children }: { children: ReactNode }) {
    const [registroDeHoy, setRegistroDeHoy] = useState<RegistroAsistenciaSalida[]>([]);
    const [ultimosEventos, setUltimosEventos] = useState<EventoReconocimiento[]>([]);
    const [errorConexion, setErrorConexion] = useState<string | null>(null);

    const refrescarRegistro = useCallback(async () => {
        try {
            const registros = await listarAsistencias();
            setRegistroDeHoy(registros);
            setErrorConexion(null);
        } catch (error) {
            const mensaje = 
                error instanceof ErrorApiAsistencia
                ? error.message
                : "No se pudo conectar con el servidor";
            setErrorConexion(mensaje);
        }
    }, []);

    const procesarFrame = useCallback(
        async (imagenBase64: string) => {
            try {
                const resultado = await reconocerFrame(imagenBase64);
                setErrorConexion(null);

                setUltimosEventos((previos) => {
                    const nuevoEvento: EventoReconocimiento = {
                        id: crypto.randomUUID(),
                        resultado,
                        timestamp: new Date(),
                    };
                    return [nuevoEvento, ...previos].slice(0, MAX_EVENTOS_EN_FEED);
                });

                if (resultado.reconocido) {
                    await refrescarRegistro();
                } 
            } catch (error) {
                const mensaje =
                    error instanceof ErrorApiAsistencia
                    ? error.message
                    : "No s epudo conectar con el servidor.";
                setErrorConexion(mensaje);
            }
        },
        [refrescarRegistro]
    );

    return (
        <AsistenciaContext.Provider
            value={{
                registroDeHoy,
                ultimosEventos,
                errorConexion,
                procesarFrame,
                refrescarRegistro,
            }}
        >
            {children}
        </AsistenciaContext.Provider>
    );
}

export function useAsistencia(): AsistenciaContextvalue {
    const contexto = useContext(AsistenciaContext);
    if (contexto === undefined) {
        throw new Error("useAsistencia debe usarse dentro de un AsistenciaProvider.");
    }
    return contexto;
}