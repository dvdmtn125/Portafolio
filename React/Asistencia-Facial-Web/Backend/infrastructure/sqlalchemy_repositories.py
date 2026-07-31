from datetime import date, datetime

import numpy as np
from sqlalchemy import Date, DateTime, Float, LargeBinary, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from domain.entities import Persona, RegistroAsistencia
from domain.ports import RepositorioAsistenciaPort, RepositorioPersonasPort

DIMENSION_ENCODING = 128
DTYPE_ENCODING = np.float64


class Base(DeclarativeBase):
    pass


class PersonaModel(Base):
    __tablename__ = "personas"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    encoding_facial: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)


class RegistroAsistenciaModel(Base):
    __tablename__ = "registros_asistencia"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    persona_id: Mapped[str] = mapped_column(String, nullable=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    momento: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    confianza: Mapped[float] = mapped_column(Float, nullable=False)


def crear_engine_sqlite(ruta_db: str = "asistencia.db"):
    engine = create_engine(f"sqlite:///{ruta_db}")
    Base.metadata.create_all(engine)
    return engine


class ErrorEncodingCorrupto(Exception):
    """Se lanza cuando un encoding almacenado no tiene la dimensión esperada"""

class RepositorioPersonasSQLAlchemy(RepositorioPersonasPort):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def guardar(self, persona: Persona) -> None:
        with self._session_factory() as session:
            modelo = PersonaModel(
                id=persona.id,
                nombre=persona.nombre,
                encoding_facial=persona.encoding_facial.tobytes(),
            )
            session.merge(modelo)
            session.commit()

    def listar_todas(self) -> list[Persona]:
        with self._session_factory() as session:
            modelos = session.query(PersonaModel).all()
            return [self._a_entidad(m) for m in modelos]

    def buscar_por_id(self, persona_id: str) -> Persona | None:
        with self._session_factory() as session:
            modelo = session.get(PersonaModel, persona_id)
            return self._a_entidad(modelo) if modelo else None

    @staticmethod
    def _a_entidad(modelo: PersonaModel) -> Persona:
        encoding = np.frombuffer(modelo.encoding_facial, dtype=DTYPE_ENCODING)

        if encoding.shape[0] != DIMENSION_ENCODING:
            raise ErrorEncodingCorrupto(
                f"El encoding de '{modelo.id}' tiene {encoding.shape[0]} elementos, "
                f"se esperaban {DIMENSION_ENCODING}. Posible dtype incorrecto o dato dañado."
            )
        return Persona(
            id=modelo.id,
            nombre=modelo.nombre,
            encoding_facial=encoding,
        )


class RepositorioAsistenciaSQLAlchemy(RepositorioAsistenciaPort):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def registrar(self, registro: RegistroAsistencia) -> None:
        with self._session_factory() as session:
            modelo = RegistroAsistenciaModel(
                persona_id=registro.persona_id,
                nombre=registro.nombre,
                momento=registro.momento,
                fecha=registro.momento.date(),
                confianza=registro.confianza,
            )
            session.add(modelo)
            session.commit()

    def ya_registrado_hoy(self, persona_id: str) -> bool:
        with self._session_factory() as session:
            existe = (
                session.query(RegistroAsistenciaModel)
                .filter_by(persona_id=persona_id, fecha=date.today())
                .first()
            )
            return existe is not None

    def listar_por_fecha(self, fecha: date) -> list[RegistroAsistencia]:
        with self._session_factory() as session:
            modelos = (
                session.query(RegistroAsistenciaModel).filter_by(fecha=fecha).all()
            )
            return [
                RegistroAsistencia(
                    persona_id=m.persona_id,
                    nombre=m.nombre,
                    momento=m.momento,
                    confianza=m.confianza,
                )
                for m in modelos
            ]