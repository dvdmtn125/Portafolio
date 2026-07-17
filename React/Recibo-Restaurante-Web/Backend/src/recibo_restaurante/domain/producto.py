from dataclasses import dataclass



@dataclass
class Producto:
    nombre: str
    precio: float
    categoria_id: int
    id: int | None = None

    def __post_init__(self) -> None:
        if not self.nombre.strip():
            raise ValueError('El nombre del producto no puede estar vacío.')
        if self.precio <= 0:
            raise ValueError('El precio debe ser mayor a cero.')
        if self.categoria_id <= 0:
            raise ValueError('El categoria_id debe de ser un entero positivo.')