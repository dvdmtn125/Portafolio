import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { AsistenciaProvider, useAsistencia } from "./AsistenciaContext";
import * as api from "../services/asistenciaApi";
import { ErrorApiAsistencia } from "../services/asistenciaApi";
import type { ReconocimientoSalida, RegistroAsistenciaSalida } from "../types/asistencia";

vi.mock("../services/asistenciaApi", async () =>{
    const actual = await vi.importActual<typeof api>("../services/asistenciaApi");
    return {
        ...actual,
        reconocerFrame: vi.fn(),
        listarAsistencias: vi.fn(),
    };
});


function ConsumidorDePrueba() {
    const { ultimosEventos, registroDeHoy, errorConexion, procesarFrame, refrescarRegistro } = 
        useAsistencia();

    return (
        <div>
            <button onClick={() => procesarFrame("frame-falso")}>Procesar frame</button>
            <button onClick={() => refrescarRegistro()}>Refrescar</button>
            <p data-testid="cantidad-eventos">{ultimosEventos.length}</p>
            <p data-testid="cantidad-registros">{registroDeHoy.length}</p>
            <p data-testid="error">{errorConexion ?? "sin-error"}</p>
        </div>
    );
}

function renderizarConProvider() {
    return render(
        <AsistenciaProvider>
            <ConsumidorDePrueba />
        </AsistenciaProvider>
    );
}

describe("AsistenciaContext", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it("agrega un evento al feed cuando procesarFrame tiene éxito", async () => {
        const resultado: ReconocimientoSalida = {
            reconocido: false,
            persona_id: null,
            nombre: null,
            confianza: 0.0,
        };
        vi.mocked(api.reconocerFrame).mockResolvedValue(resultado);

        renderizarConProvider();
        const usuario = userEvent.setup();
        await usuario.click(screen.getByText("Procesar frame"));
        
        await waitFor(() => {
            expect(screen.getByTestId("cantidad-eventos").textContent).toBe("1");
        });
    });

    it("refresca los registros del día cuando el reconocimiento es exitoso", async () => {
        const resultado: ReconocimientoSalida = {
            reconocido: true,
            persona_id: "p1",
            nombre: "Ana Torres",
            confianza: 0.9,
        };
        const registro: RegistroAsistenciaSalida[] = [
            { persona_id: "p1", nombre: "Ana Torres", momento: "2026-08-09T10:00:00", confianza: 0.9},
        ];
        vi.mocked(api.reconocerFrame).mockResolvedValue(resultado);
        vi.mocked(api.listarAsistencias).mockResolvedValue(registro);

        renderizarConProvider();
        const usuario = userEvent.setup();
        await usuario.click(screen.getByText("Procesar frame"));

        await waitFor(() => {
            expect(screen.getByTestId("cantidad-registros").textContent).toBe("1");
        });
        expect(api.listarAsistencias).toHaveBeenCalledTimes(1);
    });

    it("no refresca los registros cuando no hay reconocimiento", async () => {
        const resultado: ReconocimientoSalida = {
            reconocido: false,
            persona_id: null,
            nombre: null,
            confianza: 0.0,
        };
        vi.mocked(api.reconocerFrame).mockResolvedValue(resultado);

        renderizarConProvider();
        const usuario = userEvent.setup();
        await usuario.click(screen.getByText("Procesar frame"));

        await waitFor(() => {
            expect(screen.getByTestId("cantidad-eventos").textContent).toBe("1");
        });
        expect(api.listarAsistencias).not.toHaveBeenCalled();
    });

    it("establece errorConexion cuando procesarFrame falla", async () => {
        vi.mocked(api.reconocerFrame).mockRejectedValue(
            new ErrorApiAsistencia("Servidor no disponible", 500)
        );

        renderizarConProvider();
        const usuario = userEvent.setup();
        await usuario.click(screen.getByText("Procesar frame"));

        await waitFor(() => {
            expect(screen.getByTestId("error").textContent).toBe("Servidor no disponible");
        });
    });

    it("limpia errorConexion en el siguiente éxito tras un error previo", async () => {
        vi.mocked(api.reconocerFrame)
            .mockRejectedValueOnce(new ErrorApiAsistencia("Servidor no disponible", 500))
            .mockResolvedValueOnce({
                reconocido: false,
                persona_id: null,
                nombre: null,
                confianza: 0.0,
            });

        renderizarConProvider();
        const usuario = userEvent.setup();

        await usuario.click(screen.getByText("Procesar frame"));
        await waitFor(() => {
            expect(screen.getByTestId("error").textContent).toBe("Servidor no disponible");
        });

        await usuario.click(screen.getByText("Procesar frame"));
        await waitFor(() => {
            expect(screen.getByTestId("error").textContent).toBe("sin-error");
        });
    });

    it("lanza un error si useAsistencia se usa fuera del provider", () => {
        const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});

        function ComponenteSinProvider() {
            useAsistencia();
            return null;
        }

        expect(() => render(<ComponenteSinProvider />)).toThrow(
            "useAsistencia debe usarse dentro de un AsistenciaProvider."
        );
    });
});