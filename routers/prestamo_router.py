from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import obtener_session
from models.prestamo import Prestamo, PrestamoCreacion
from services.prestamo_service import registrar_prestamo, registrar_devolucion

router = APIRouter(prefix="/prestamos", tags=["Prestamos"])


@router.post("/", status_code=201, response_model=Prestamo)
def crear_prestamo(datos: PrestamoCreacion, session: Session = Depends(obtener_session)):
    return registrar_prestamo(session, datos)


@router.post("/{id}/devolucion", response_model=Prestamo)
def devolver_prestamo(id: int, session: Session = Depends(obtener_session)):
    return registrar_devolucion(session, id)
