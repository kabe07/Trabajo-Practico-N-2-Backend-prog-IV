from sqlmodel import Session, select
from models.socio import Socio


def buscar_socio_por_id(session: Session, socio_id: int):
    return session.get(Socio, socio_id)


def listar_socios(session: Session):
    return session.exec(select(Socio)).all()


def guardar_socio(session: Session, socio: Socio):
    session.add(socio)
    session.flush()
    return socio


def eliminar_socio(session: Session, socio: Socio):
    session.delete(socio)
