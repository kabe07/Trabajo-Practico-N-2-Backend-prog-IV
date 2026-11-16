from sqlmodel import Session, select
from models.prestamo import Prestamo


def buscar_prestamo_por_id(session: Session, prestamo_id: int):
    return session.get(Prestamo, prestamo_id)


def listar_prestamos_socio(session: Session, socio_id: int, activos: bool = False):
    consulta = select(Prestamo).where(Prestamo.socio_id == socio_id)
    if activos:
        consulta = consulta.where(Prestamo.fecha_devolucion.is_(None))
    return session.exec(consulta).all()


def guardar_prestamo(session: Session, prestamo: Prestamo):
    session.add(prestamo)
    session.flush()
    return prestamo


def hay_prestamos_libro(session: Session, libro_id: int):
    return session.exec(select(Prestamo).where(Prestamo.libro_id == libro_id)).first() is not None
