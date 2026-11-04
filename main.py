from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import crear_tablas

@asynccontextmanager
async def lifespan(app:FastAPI):
    crear_tablas()
    yield #Todo lo que se codea antes de yield se ejecuta al comenzar la aplicacion y lo que se codea despues al finalizar.

app=FastAPI(lifespan=lifespan)#Llamamos a crear las tablas cuando se inicie la aplicacion

@app.get("/")
def inicio():
    return {"mensaje":"API de Biblioteca"}
