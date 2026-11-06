from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import obtener_session
from models.autor import Autor
from services.autor_service import crear_autor, obtener_autores, obtener_autor_por_id


router=APIRouter(prefix="/autores", tags=["Autores"])

@router.post("/", status_code=201) #Recibe una peticion post en autores
def registrar_autor(
    autor:Autor,  #Recibe los datos del autor
    session:Session=Depends(obtener_session) #FastAPI, antes de ejecutar esta función, usá obtener_session para conseguir una sesión y pasámela en el parámetro session”
):
    return crear_autor(session, autor)

@router.get("/")
def listar_autores(session: Session= Depends(obtener_session)):
    return obtener_autores(session)


@router.get("/{autor_id}") #{autor_id} es una parte variable de la ruta. Por ejemplo, en GET /autores/556, FastAPI toma 556 y lo entrega al parámetro autor_id
def consultar_autor(
    autor_id:int,
    session: Session=Depends (obtener_session),#Con Depends le estamos pasando la función a FastAPI para que la ejecute cuando corresponda
):
    return obtener_autor_por_id(session, autor_id)


