export interface ReconocimientoSalida {
    reconocido: boolean;
    persona_id: string | null;
    nombre: string | null;
    confianza: number;
}

export interface RegistroAsistenciaSalida {
    persona_id: string;
    nombre: string;
    momento: string;
    confianza: number;
}

export interface PersonaSalida {
    id: string;
    nombre: string;
}