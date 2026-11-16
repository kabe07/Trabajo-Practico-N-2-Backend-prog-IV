from fastapi import HTTPException
from sqlmodel import Session
from repositories.libro_repository import (
    buscar_asociaciones,
    buscar_libro_por_id,
    guardar_asociaciones,
    listar_libros,
)
from sqlalchemy.exc import IntegrityError

from models.libro import Libro, LibroCreacion
from repositories.libro_repository import guardar_libro

from services.autor_service import obtener_autor_por_id

def asociar_autor_a_libro(session:Session, libro_id:int, autor_id:int):
    if buscar_libro_por_id(session,libro_id) is None:
        raise HTTPException(status_code=404, detail="Libro no Encontrado")
    obtener_autor_por_id(session,autor_id)

    if buscar_asociaciones(session,libro_id,autor_id) is not None:
        raise HTTPException(status_code=409,detail="El autor ya esta asociado al libro")

    asociacion=guardar_asociaciones(session,libro_id,autor_id)
    session.commit()
    session.refresh(asociacion)
    return asociacion

def crear_libro(session:Session, datos:LibroCreacion):
    libro=Libro(
        titulo=datos.titulo,
        ISBN=datos.isbn,
        stock=datos.stock,
    )
    try:
        guardar_libro(session,libro)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe un Libro con ese ISBN"
        )
    session.refresh(libro)
    return libro

def obtener_libros(session: Session, disponibles: bool = False):
    return listar_libros(session, disponibles)

def obtener_libro_por_id(session: Session, libro_id: int):
    libro = buscar_libro_por_id(session, libro_id)

    if libro is None:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado",
        )

    return libro