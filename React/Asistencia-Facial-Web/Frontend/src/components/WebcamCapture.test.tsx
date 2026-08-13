import { describe, it,expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { WebcamCapture } from "./WebcamCapture";
import { AsistenciaProvider } from "../context/AsistenciaContext";
import * as api from "../services/asistenciaApi";

vi.mock("../services/asistenciaApi", async () => {
    const actual = await vi.importActual<typeof api>("../services/asistenciaApi");
    return {
        ...actual,
        reconocerFrame: vi.fn(),
        listarAsistencias: vi.fn(),
    };
});

function renderizarConProvider() {
    return render(
        <AsistenciaProvider>
            <WebcamCapture />
        </AsistenciaProvider>
    );
}

describe("WebcamCapture", () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.mocked(api.listarAsistencias).mockResolvedValue([]);
    });

    it("muestra el botón de iniciar camara antes de activarla", () => {
        renderizarConProvider();
        expect(screen.getByText("Iniciar cámara")).toBeInTheDocument();
    });

    it("activa la cámara y muestra el botón de detener al hacer clic", async () => {
        renderizarConProvider();
        const usuario = userEvent.setup();

        await usuario.click(screen.getByText("Iniciar cámara"));

        await waitFor(() => {
            expect(screen.getByText("Detener cámara")).toBeInTheDocument();
        });
        expect(navigator.mediaDevices.getUserMedia).toHaveBeenCalledTimes(1);
    });

    it("muestra un mensaje de error si getUserMedia es rechazado", async () => {
        vi.mocked(navigator.mediaDevices.getUserMedia).mockRejectedValueOnce(
            new Error("Permiso denegado")
        );

        renderizarConProvider();
        const usuario = userEvent.setup();
        await usuario.click(screen.getByText("Iniciar cámara"));

        await waitFor(() => {
            expect(
                screen.getByText(/No se pudo acceder a la cámara/i)
            ).toBeInTheDocument();
        });
    });

    it("detener la cámara y vuelve a mostrar el boton de iniciar", async () => {
        renderizarConProvider();
        const usuario = userEvent.setup();

        await usuario.click(screen.getByText("Iniciar cámara"));
        await waitFor(() => {
            expect(screen.getByText("Iniciar cámara")).toBeInTheDocument();
        });
    });

    it("procesa un frame automáticamente tras el intervalo de captura", async () => {
        vi.useFakeTimers();
        vi.mocked(api.reconocerFrame).mockResolvedValue({
            reconocido: false,
            persona_id: null,
            nombre: null,
            confianza: 0.0,
        });

        renderizarConProvider();
        const usuario = userEvent.setup({ delay: null });

        await usuario.click(screen.getByText("Iniciar cámara"));

        await vi.advanceTimersByTimeAsync(2500);

        expect(api.reconocerFrame).toHaveBeenCalledTimes(1);

        vi.useRealTimers();
    });
});