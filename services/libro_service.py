from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from models.libro import Libro, LibroCreacion, LibroActualizacion, LibroRespuesta
from repositories.libro_repository import (
    buscar_asociaciones, buscar_libro_por_id, guardar_asociaciones,
    guardar_libro, listar_libros, obtener_autores_libro, eliminar_libro,
)
from repositories.prestamo_repository import hay_prestamos_libro
from services.autor_service import obtener_autor_por_id


def obtener_libro_por_id(session: Session, libro_id: int):
    libro = buscar_libro_por_id(session, libro_id)
    if libro is None:
        raise HTTPException(404, "Libro no encontrado")
    return libro


def respuesta_libro(session: Session, libro: Libro):
    return LibroRespuesta(
        **libro.model_dump(), autores=obtener_autores_libro(session, libro.id)
    )


def obtener_libros(session: Session, disponibles: bool = False):
    return [respuesta_libro(session, libro) for libro in listar_libros(session, disponibles)]


def crear_libro(session: Session, datos: LibroCreacion):
    libro = Libro(**datos.model_dump())
    try:
        guardar_libro(session, libro)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Ya existe un libro con ese ISBN")
    session.refresh(libro)
    return respuesta_libro(session, libro)


def actualizar_libro(session: Session, libro_id: int, datos: LibroActualizacion):
    libro = obtener_libro_por_id(session, libro_id)
    for campo, valor in datos.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(libro, campo, valor)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Ya existe un libro con ese ISBN")
    session.refresh(libro)
    return respuesta_libro(session, libro)


def asociar_autor_a_libro(session: Session, libro_id: int, autor_id: int):
    obtener_libro_por_id(session, libro_id)
    obtener_autor_por_id(session, autor_id)
    if buscar_asociaciones(session, libro_id, autor_id) is not None:
        raise HTTPException(409, "El autor ya esta asociado al libro")
    try:
        asociacion = guardar_asociaciones(session, libro_id, autor_id)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "No se pudo crear la asociacion")
    session.refresh(asociacion)
    return asociacion


def borrar_libro(session: Session, libro_id: int):
    libro = obtener_libro_por_id(session, libro_id)
    if hay_prestamos_libro(session, libro_id):
        raise HTTPException(409, "El libro tiene prestamos registrados")
    eliminar_libro(session, libro)
    session.commit()
