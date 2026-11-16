from fastapi import HTTPException
from sqlmodel import Session, select
from models.autor import Autor, AutorCreacion, AutorActualizacion
from models.libro_autor import Libro_Autor
from repositories.autor_repository import (
    guardar_autor, listar_autores, eliminar_autor, buscar_autor_por_id,
)


def crear_autor(session: Session, datos: AutorCreacion):
    autor = Autor(**datos.model_dump())
    guardar_autor(session, autor)
    session.commit()
    session.refresh(autor)
    return autor


def obtener_autores(session: Session):
    return listar_autores(session)


def obtener_autor_por_id(session: Session, autor_id: int):
    autor = buscar_autor_por_id(session, autor_id)
    if autor is None:
        raise HTTPException(404, "Autor no encontrado")
    return autor


def actualizar_autor(session: Session, autor_id: int, datos: AutorActualizacion):
    autor = obtener_autor_por_id(session, autor_id)
    for campo, valor in datos.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(autor, campo, valor)
    session.commit()
    session.refresh(autor)
    return autor


def borrar_autor(session: Session, autor_id: int) -> None:
    autor = obtener_autor_por_id(session, autor_id)
    asociaciones = session.exec(
        select(Libro_Autor).where(Libro_Autor.autor_id == autor_id)
    ).all()
    for asociacion in asociaciones:
        session.delete(asociacion)
    session.flush()
    eliminar_autor(session, autor)
    session.commit()
