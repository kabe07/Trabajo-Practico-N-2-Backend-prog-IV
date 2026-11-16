from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import crear_tablas
from routers.autor_router import router as autor_router
from routers.libro_router import router as libro_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    crear_tablas()
    yield #Todo lo que se codea antes de yield se ejecuta al comenzar la aplicacion y lo que se codea despues al finalizar.

app=FastAPI(lifespan=lifespan)#Llamamos a crear las tablas cuando se inicie la aplicacion
app.include_router(autor_router)
app.include_router(libro_router)

@app.get("/")
def inicio():
    return {"mensaje":"API de Biblioteca"}
