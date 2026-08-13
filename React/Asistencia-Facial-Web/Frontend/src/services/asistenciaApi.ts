import type {
    PersonaSalida,
    ReconocimientoSalida,
    RegistroAsistenciaSalida,
} from "../types/asistencia";

const API_BASE_URL = "http://127.0.0.1:8000";

export class ErrorApiAsistencia extends Error {
    status: number;

    constructor(mensaje: string, status: number) {
        super(mensaje);
        this.status = status;
        this.name = "ErrorApiAsistencia";
    }
}

async function manejarRespuesta<T>(respuesta: Response): Promise<T> {
    if (!respuesta.ok) {
        let detalle = `Error ${respuesta.status}`
        try {
            const cuerpo = await respuesta.json();
            detalle = cuerpo.detail ?? detalle;
        } catch {
            // mensaje genérico
        }
        throw new ErrorApiAsistencia(detalle, respuesta.status);
    }
    return respuesta.json() as Promise<T>;
}

export async function reconocerFrame(
    imagenBase64: string
): Promise<ReconocimientoSalida> {
    const respuesta = await fetch(`${API_BASE_URL}/asistencia/reconocer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ imagen_base64: imagenBase64 }),
    });
    return manejarRespuesta<ReconocimientoSalida>(respuesta);
}

export async function listarAsistencias(
    fecha?: string
): Promise<RegistroAsistenciaSalida[]> {
    const url = new URL(`${API_BASE_URL}/asistencia`);
    if (fecha) {
        url.searchParams.set("fecha", fecha);
    }
    const respuesta = await fetch(url);
    return manejarRespuesta<RegistroAsistenciaSalida[]>(respuesta);
}

export async function registrarPersona(
    id: string,
    nombre: string,
    imagen: Blob
): Promise<PersonaSalida> {
    const formData = new FormData();
    formData.append("id", id);
    formData.append("nombre", nombre);
    formData.append("imagen", imagen, "captura.jpg");

    const respuesta = await fetch(`${API_BASE_URL}/personas`, {
        method: "POST",
        body: formData,
    });
    return manejarRespuesta<PersonaSalida>(respuesta);
}