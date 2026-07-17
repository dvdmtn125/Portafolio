from sqlalchemy.orm import Session

from recibo_restaurante.application.interfaces.repositorio_categorias import RepositorioCategorias
from recibo_restaurante.domain.categoria import Categoria
from recibo_restaurante.infrastructure.db.modelos import CategoriaModelo


class RepositorioCategoriasSQLAlchemy(RepositorioCategorias):
    def __init__(self, sesion: Session) -> None:
        self._sesion = sesion

    def listar(self) -> list[Categoria]:
        modelos = self._sesion.query(CategoriaModelo).all()
        return[self._a_entidad(modelo) for modelo in modelos]
    
    def obtener_por_id(self, categoria_id: int) -> Categoria | None:
        modelo = self._sesion.get(CategoriaModelo, categoria_id)
        return self._a_entidad(modelo) if modelo else None
    
    def crear(self, categoria: Categoria) -> Categoria:
        modelo = CategoriaModelo(nombre=categoria.nombre)
        self._sesion.add(modelo)
        self._sesion.commit()
        self._sesion.refresh(modelo)
        return self._a_entidad(modelo)
    
    def eliminar(self, categoria_id: int) -> Categoria:
        modelo = self._sesion.get(CategoriaModelo, categoria_id)
        if modelo is not None:
            self._sesion.delete(modelo)
            self._sesion.commit()

    def _a_entidad(self, modelo: CategoriaModelo) -> Categoria:
        return Categoria(id=modelo.id, nombre=modelo.nombre)