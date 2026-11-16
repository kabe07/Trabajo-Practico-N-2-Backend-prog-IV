from datetime import date, timedelta
from fastapi import HTTPException
from sqlmodel import Session
from models.prestamo import Prestamo, PrestamoCreacion
from repositories.prestamo_repository import (
    buscar_prestamo_por_id, listar_prestamos_socio, guardar_prestamo,
)
from services.libro_service import obtener_libro_por_id
from services.socio_service import obtener_socio_por_id


def registrar_prestamo(session: Session, datos: PrestamoCreacion):
    # SQLite reserva la escritura antes de leer stock y prestamos activos.
    # Asi dos peticiones simultaneas no pueden prestar el ultimo ejemplar.
    with session.begin():
        session.connection().exec_driver_sql("BEGIN IMMEDIATE")
        socio = obtener_socio_por_id(session, datos.socio_id)
        libro = obtener_libro_por_id(session, datos.libro_id)
        if not socio.activo:
            raise HTTPException(403, "El socio esta inactivo")
        if len(listar_prestamos_socio(session, socio.id, activos=True)) >= 3:
            raise HTTPException(409, "El socio ya tiene 3 prestamos activos")
        if libro.stock <= 0:
            raise HTTPException(409, "El libro no tiene stock")
        hoy = date.today()
        prestamo = Prestamo(
            socio_id=socio.id, libro_id=libro.id,
            fecha_prestamo=hoy, fecha_vencimiento=hoy + timedelta(days=14),
        )
        libro.stock -= 1
        guardar_prestamo(session, prestamo)
    session.refresh(prestamo)
    return prestamo


def registrar_devolucion(session: Session, prestamo_id: int):
    with session.begin():
        session.connection().exec_driver_sql("BEGIN IMMEDIATE")
        prestamo = buscar_prestamo_por_id(session, prestamo_id)
        if prestamo is None:
            raise HTTPException(404, "Prestamo no encontrado")
        if prestamo.fecha_devolucion is not None:
            raise HTTPException(409, "El prestamo ya fue devuelto")
        libro = obtener_libro_por_id(session, prestamo.libro_id)
        hoy = date.today()
        prestamo.fecha_devolucion = hoy
        prestamo.multa = max(0, (hoy - prestamo.fecha_vencimiento).days) * 100
        libro.stock += 1
    session.refresh(prestamo)
    return prestamo
