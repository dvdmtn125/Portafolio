from pydantic import BaseModel, ConfigDict


class ProductoCrear(BaseModel):
    nombre: str
    precio: float
    categoria_id: int


class ProductoActualizar(BaseModel):
    nombre: str
    precio: float
    categoria_id: int


class ProductoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    precio: float
    categoria_id: int