from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import crear_tablas
from routers.autor_router import router as autor_router
from routers.libro_router import router as libro_router
from routers.socio_router import router as socio_router
from routers.prestamo_router import router as prestamo_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield


app = FastAPI(title="API de Biblioteca", lifespan=lifespan)
app.include_router(autor_router)
app.include_router(libro_router)
app.include_router(socio_router)
app.include_router(prestamo_router)


@app.get("/")
def inicio():
    return {"mensaje": "API de Biblioteca"}
