from fastapi import HTTPException
from sqlmodel import Session
from repositories.libro_repository import (
    buscar_asociaciones,
    buscar_libro_por_id,
    guardar_asociaciones,
)

from services.autor_service import obtener_autor_por_id

def asociar_autor_a_libro(session:Session, libro_id:int, autor_id:int):
    if buscar_libro_por_id(session,libro_id) is None:
        raise HTTPException(status_code=404, detail="Libro no Encontrado")
    obtener_autor_por_id(session,autor_id)

    if buscar_asociaciones(session,libro_id,autor_id) is not None:
        raise HTTPException(status_code=409,detail="El autor ya esta asociado al libro")

    asociacion=guardar_asociaciones(session,autor_id,libro_id)
    session.commit()
    session.refresh(asociacion)
    return asociacion
