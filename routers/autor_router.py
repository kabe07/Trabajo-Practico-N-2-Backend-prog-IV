from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import obtener_session
from models.autor import Autor, AutorCreacion, AutorActualizacion
from services.autor_service import (
    crear_autor, obtener_autores, obtener_autor_por_id, actualizar_autor, borrar_autor,
)

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.post("/", status_code=201, response_model=Autor)
def registrar_autor(datos: AutorCreacion, session: Session = Depends(obtener_session)):
    return crear_autor(session, datos)


@router.get("/", response_model=list[Autor])
def listar_autores(session: Session = Depends(obtener_session)):
    return obtener_autores(session)


@router.get("/{autor_id}", response_model=Autor)
def consultar_autor(autor_id: int, session: Session = Depends(obtener_session)):
    return obtener_autor_por_id(session, autor_id)


@router.patch("/{autor_id}", response_model=Autor)
def modificar_autor(autor_id: int, datos: AutorActualizacion, session: Session = Depends(obtener_session)):
    return actualizar_autor(session, autor_id, datos)


@router.delete("/{autor_id}", status_code=204)
def eliminar_autor(autor_id: int, session: Session = Depends(obtener_session)) -> None:
    borrar_autor(session, autor_id)
