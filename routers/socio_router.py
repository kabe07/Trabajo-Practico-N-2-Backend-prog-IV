from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import obtener_session
from models.socio import Socio, SocioCreacion, SocioActualizacion
from models.prestamo import Prestamo
from services.socio_service import (
    crear_socio, obtener_socios, obtener_socio_por_id,
    actualizar_socio, borrar_socio, obtener_prestamos_socio,
)

router = APIRouter(prefix="/socios", tags=["Socios"])


@router.post("/", status_code=201, response_model=Socio)
def registrar_socio(datos: SocioCreacion, session: Session = Depends(obtener_session)):
    return crear_socio(session, datos)


@router.get("/", response_model=list[Socio])
def consultar_socios(session: Session = Depends(obtener_session)):
    return obtener_socios(session)


@router.get("/{id}", response_model=Socio)
def consultar_socio(id: int, session: Session = Depends(obtener_session)):
    return obtener_socio_por_id(session, id)


@router.patch("/{id}", response_model=Socio)
def modificar_socio(id: int, datos: SocioActualizacion, session: Session = Depends(obtener_session)):
    return actualizar_socio(session, id, datos)


@router.delete("/{id}", status_code=204)
def eliminar_socio(id: int, session: Session = Depends(obtener_session)) -> None:
    borrar_socio(session, id)


@router.get("/{id}/prestamos", response_model=list[Prestamo])
def consultar_prestamos(id: int, activos: bool = False, session: Session = Depends(obtener_session)):
    return obtener_prestamos_socio(session, id, activos)
