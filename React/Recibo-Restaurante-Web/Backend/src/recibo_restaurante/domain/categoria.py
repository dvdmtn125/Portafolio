from dataclasses import dataclass


@dataclass
class Categoria:
    nombre: str
    id: int | None = None

    def __post_init__(self) -> None:
        if not self.nombre.strip():
            raise ValueError('El nombre de la categoria no puede estar vació.')