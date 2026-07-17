from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from recibo_restaurante.infrastructure.db.modelos import Base

MOTOR = create_engine('sqlite:///recibo_restaurante.db')
SesionLocal = sessionmaker(bind=MOTOR)


def crear_tablas() -> None:
    Base.metadata.create_all(bind=MOTOR)