from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from recibo_restaurante.controllers.routers import categorias, facturacion, productos
from recibo_restaurante.infrastructure.db.sesion import crear_tablas

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield


app = FastAPI(title='Recibo Restaurante API', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(facturacion.router)