from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class CategoriaModelo(Base):
    __tablename__ = 'categorias'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    
    productos: Mapped[list['ProductoModelo']] = relationship(back_populates='categoria')


class ProductoModelo(Base):
    __tablename__ = 'productos'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    precio: Mapped[float]
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.id'))

    categoria: Mapped['CategoriaModelo'] = relationship(back_populates='productos')