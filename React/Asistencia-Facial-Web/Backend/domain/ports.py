from abc import ABC, abstractmethod

from domain.entities import Persona, RegistroAsistencia, ResultadoReconocimiento


class ReconocedorFacialPort(ABC):
    """Puerto para cualquier motor de reconocimiento facial (face_recognition, otro futuro)."""

    @abstractmethod
    def reconocer(
        self, imagen_bytes: bytes, personas_conocidas: list[Persona]
    ) -> ResultadoReconocimiento:
        """Recibe una imagen cruda y la lista de personas conocidas, devuelve el resultado."""
        ...

    @abstractmethod
    def calcular_encoding(self, imagen_bytes: bytes) -> "np.ndarray | None":
        """Extrae el encoding facial de una imagen, útil al registrar una persona nueva."""
        ...


class RepositorioPersonasPort(ABC):
    @abstractmethod
    def guardar(self, persona: Persona) -> None: ...

    @abstractmethod
    def listar_todas(self) -> list[Persona]: ...

    @abstractmethod
    def buscar_por_id(self, persona_id: str) -> Persona | None: ...


class RepositorioAsistenciaPort(ABC):
    @abstractmethod
    def registrar(self, registro: RegistroAsistencia) -> None: ...

    @abstractmethod
    def ya_registrado_hoy(self, perosna_id: str) -> bool:
        """Evita marcar asistencia duplicada el mismo día."""
        ...

    @abstractmethod
    def listar_por_fecha(self, fecha: "date") -> list[RegistroAsistencia]: ...