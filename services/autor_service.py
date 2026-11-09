from sqlmodel import Session
from models.autor import Autor
from repositories.autor_repository import guardar_autor, listar_autores, eliminar_autor,buscar_autor_por_id
from fastapi import HTTPException


def crear_autor(session: Session, autor: Autor): #el service coordina la operación y confirma los cambios
    guardar_autor(session, autor)
    session.commit()
    session.refresh(autor)
    return autor

def obtener_autores(session: Session):
    return listar_autores(session)

def obtener_autor_por_id(session: Session, autor_id: int):
    autor= buscar_autor_por_id(session,autor_id)
    if autor is None:
        raise HTTPException(
            status_code=404,
            detail="Autor no encontrado"
        )
    return autor

def actualizar_autor(session:Session, autor_id:int, nombre:str):
    autor=obtener_autor_por_id(session,autor_id)
    autor.nombre=nombre
    session.commit()
    session.refresh(autor)
    return autor

def borrar_autor(session: Session, autor_id: int)-> None:
    autor= obtener_autor_por_id(session, autor_id)
    eliminar_autor(session,autor)
    session.commit()

