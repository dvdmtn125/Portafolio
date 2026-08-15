import { useCallback, useEffect, useRef, useState } from "react";

import { useAsistencia } from "../context/AsistenciaContext";

const INTERVALO_CAPTURA_MS = 2500;
const ANCHO_CAPTURA = 320;
const ALTO_CAPTURA = 240;

export function WebcamCapture() {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const procesandoRef = useRef(false);

    const [camaraActiva, setCamaraActiva] = useState(false);
    const [errorCamara, setErrorCamara] = useState<string | null>(null);

    const { procesarFrame, ultimosEventos } = useAsistencia();

    const iniciarCamara = useCallback(async () => {
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
            setErrorCamara(null);
        } catch {
            setErrorCamara(
                "No se pudo acceder a la cámara. Verifica los permisos del navegador."
            );
            setCamaraActiva(false);
        }
    }, []);

    const detenerCamara = useCallback(() => {
        streamRef.current?.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
        setCamaraActiva(false);
    }, []);

    const capturarYEnviarFrame = useCallback(async () => {
        if (procesandoRef.current) return;

        const video = videoRef.current;
        const canvas = canvasRef.current;
        if (!video || !canvas) return;

        const contexto = canvas.getContext("2d");
        if (!contexto) return;

        contexto.drawImage(video, 0, 0, ANCHO_CAPTURA, ALTO_CAPTURA);

        const dataUrl = canvas.toDataURL("image/jpeg", 0.8);
        const base64Puro = dataUrl.split(",")[1];

        procesandoRef.current = true;
        try {
            await procesarFrame(base64Puro);
        } finally {
            procesandoRef.current = false;
        }
    }, [procesarFrame]);

    useEffect(() => {
        if (!camaraActiva) return;

        const intervalo = setInterval(capturarYEnviarFrame, INTERVALO_CAPTURA_MS);
        return () => clearInterval(intervalo);
    }, [camaraActiva, capturarYEnviarFrame]);

    useEffect(() => {
        return () => {
            detenerCamara();
        };
    }, [detenerCamara]);

    const ultimoEvento = ultimosEventos[0];

    return (
        <div className="flex flex-col gap-4">
            <div className="relative overflow-hiden rounded-lg border border-neutral-300">
                <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full"
                    width={ANCHO_CAPTURA}
                    height={ALTO_CAPTURA}
                />
                <canvas
                    ref={canvasRef}
                    width={ANCHO_CAPTURA}
                    height={ALTO_CAPTURA}
                    className="hidden" 
                />
            </div>

            {errorCamara && (
                <p className="text-sm text-red-600">{errorCamara}</p>
            )}

            <div className="flex gap-2">
                {!camaraActiva ? (
                    <button
                        onClick={iniciarCamara}
                        className="rounded-md bg-neutral-900 px-4 py-2 text-sm text-white"
                    >
                        Iniciar cámara
                    </button>
                ) : (
                    <button
                        onClick={detenerCamara}
                        className="rounded-md bg-neutral-900 px-4 py-2 text-sm text-white"
                    >
                        Detener cámara
                    </button>
                )}
            </div>

            {camaraActiva && ultimoEvento && (
                <p className="text-sm text-neutral-600">
                {ultimoEvento.resultado.reconocido
                    ? `Reconocido: ${ultimoEvento.resultado.nombre}`
                    : "Sin reconocimiento"}
                </p>
            )}
        </div>
    );
}