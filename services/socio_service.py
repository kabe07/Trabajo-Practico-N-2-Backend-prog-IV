from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from models.socio import Socio, SocioCreacion, SocioActualizacion
from repositories.socio_repository import (
    buscar_socio_por_id, listar_socios, guardar_socio, eliminar_socio,
)
from repositories.prestamo_repository import listar_prestamos_socio


def obtener_socio_por_id(session: Session, socio_id: int):
    socio = buscar_socio_por_id(session, socio_id)
    if socio is None:
        raise HTTPException(404, "Socio no encontrado")
    return socio


def obtener_socios(session: Session):
    return listar_socios(session)


def crear_socio(session: Session, datos: SocioCreacion):
    socio = Socio(**datos.model_dump())
    try:
        guardar_socio(session, socio)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Ya existe un socio con ese email")
    session.refresh(socio)
    return socio


def actualizar_socio(session: Session, socio_id: int, datos: SocioActualizacion):
    socio = obtener_socio_por_id(session, socio_id)
    for campo, valor in datos.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(socio, campo, valor)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Ya existe un socio con ese email")
    session.refresh(socio)
    return socio


def borrar_socio(session: Session, socio_id: int):
    socio = obtener_socio_por_id(session, socio_id)
    if listar_prestamos_socio(session, socio_id):
        raise HTTPException(409, "El socio tiene prestamos registrados")
    eliminar_socio(session, socio)
    session.commit()


def obtener_prestamos_socio(session: Session, socio_id: int, activos: bool = False):
    obtener_socio_por_id(session, socio_id)
    return listar_prestamos_socio(session, socio_id, activos)
