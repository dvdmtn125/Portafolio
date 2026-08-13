import { useRef, useState } from "react";

import { registrarPersona, ErrorApiAsistencia } from "../services/asistenciaApi";

const ANCHO_CAPTURA = 320;
const ALTO_CAPTURA = 240;

type EstadoRegistro = "inactivo" | "guardando" | "exito" | "error";

export function RegistroPersonaForm() {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const streamRef = useRef<MediaStream | null>(null);

    const [camaraActiva, setCamaraActiva] = useState(false);
    const [fotoCapturada, setFotoCapturada] = useState<Blob | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);

    const [id, setId] = useState("");
    const [nombre, setNombre] = useState("");
    const [estado, setEstado] = useState<EstadoRegistro>("inactivo");
    const [mensaje, setMensaje] = useState<string | null>(null);

    async function iniciarCamara() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: ANCHO_CAPTURA, height: ALTO_CAPTURA },
                audio: false,
            });
            streamRef.current = stream;
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
            setCamaraActiva(true);
        } catch {
            setMensaje("No se pudo acceder a la cámara");
            setEstado("error");
        }
    }

    function detenerCamara() {
        streamRef.current?.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
        setCamaraActiva(false);
    }

    function capturarFoto() {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        if (!video || !canvas) return;

        const contexto = canvas.getContext("2d");
        if (!contexto) return;

        contexto.drawImage(video, 0, 0, ANCHO_CAPTURA, ALTO_CAPTURA);

        canvas.toBlob(
            (blob) => {
                if (!blob) return;
                setFotoCapturada(blob);
                setPreviewUrl(URL.createObjectURL(blob));
            },
            "image/jpeg",
            0.9
        );

        detenerCamara();
    }

    function reiniciarCaptura() {
        if (previewUrl) URL.revokeObjectURL(previewUrl);
        setFotoCapturada(null);
        setPreviewUrl(null);
    }

    async function manejarEnvio(evento: React.FormEvent) {
        evento.preventDefault();

        if (!fotoCapturada) {
            setMensaje("Captura una foto antes de registrar.");
            setEstado("error");
            return;
        }

        setEstado("guardando");
        setMensaje(null);

        try {
            await registrarPersona(id, nombre, fotoCapturada);
            setEstado("exito");
            setMensaje(`${nombre} fue registrado correctamente.`);
            setId("");
            setNombre("");
            reiniciarCaptura();
        } catch (error) {
            const detalle = 
                error instanceof ErrorApiAsistencia
                    ? error.message
                    : "No se pudo registrar la persona.";
            setEstado("error");
            setMensaje(detalle);
        }
    }

    return (
        <form onSubmit={manejarEnvio} className="flex flex-col gap-4">
            <h2 className="text-sm font-medium text-neutral-500">
                Registrar persona
            </h2>

            <div className="flex flex-col gap-2">
                <label className="text-sm text-neutral-600">
                    Identificador
                    <input
                        type="text"
                        value={id}
                        onChange={(evento) => setId(evento.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border border-neutral-300 px-3 py-2 text-sm"
                    />
                </label>

                <label className="text-sm text-neutral-600">
                    Nombre completo
                    <input
                        type="text"
                        value={nombre}
                        onChange={(evento) => setNombre(evento.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border border-neutral-300 px-3 py-2 text-sm"
                    />
                </label>
            </div>

            <div className="overflow-hidden rounded-lg border border-neutral-300 bg-black">
                {previewUrl ? (
                    <img src={previewUrl} alt="Foto capturada para el registro" className="w-full" />
                ) : (
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className="w-full"
                        width={ANCHO_CAPTURA}
                        height={ALTO_CAPTURA}
                    />
                )}
                <canvas
                    ref={canvasRef}
                    width={ANCHO_CAPTURA}
                    height={ALTO_CAPTURA}
                    className="hidden"
                />
            </div>

            <div className="flex gap-2">
                {!previewUrl && !camaraActiva && (
                    <button
                        type="button"
                        onClick={iniciarCamara}
                        className="rounded-md border border-neutral-300 px-4 py-2 text-sm"
                    >
                        Activar cámara
                    </button>
                )}

                {camaraActiva && !previewUrl && (
                    <button
                        type="button"
                        onClick={capturarFoto}
                        className="rounded-md bg-neutral-900 px-4 py-2 text-sm text-white"
                    >
                        Capturar foto
                    </button>
                )}

                {previewUrl && (
                    <button
                        type="button"
                        onClick={reiniciarCaptura}
                        className="rounded-md border border-neutral-300 px-4 py-2 text-sm"
                    >
                        Repetir foto
                    </button>
                )}
            </div>

            <button
                type="submit"
                disabled={estado === "guardando"}
                className="rounded-md bg-neutral-900 px-4 py-2 text-sm text-white disabled:opacity-50"
            >
                {estado === "guardando" ? "Guardando..." : "Registrar"}
            </button>

            {mensaje && (
                <p
                    className={
                        estado === "exito" ? "text-green-600" : "text-sm text-red-600"
                    }
                >
                    {mensaje}
                </p>
            )}
        </form>
    );
}