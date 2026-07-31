from datetime import date

from domain.entities import RegistroAsistencia
from domain.ports import RepositorioAsistenciaPort


class ConsultarAsistencias:
    def __init__(self, repositorio_asistencia: RepositorioAsistenciaPort):
        self._repositorio_asistencia = repositorio_asistencia

    def ejecutar(self, fecha: date | None = None) -> list[RegistroAsistencia]:
        fecha_consulta = fecha or date.today()
        return self._repositorio_asistencia.listar_por_fecha(fecha_consulta)