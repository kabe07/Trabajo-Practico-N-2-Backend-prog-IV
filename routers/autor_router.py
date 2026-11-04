from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import obtener_session
from models.autor import Autor
from services.autor_service import crear_autor


router=APIRouter(prefix="/autores", tags=["Autores"])

@router.post("/", status_code=201) #Recibe una peticion post en autores
def registrar_autor(
    autor:Autor,  #Recibe los datos del autor
    session:Session=Depends(obtener_session) #FastAPI, antes de ejecutar esta función, usá obtener_session para conseguir una sesión y pasámela en el parámetro session”
):
    return crear_autor(session, autor)
