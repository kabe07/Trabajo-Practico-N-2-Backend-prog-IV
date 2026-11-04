from sqlmodel import Session
from models.autor import Autor
from repositories.autor_repository import guardar_autor


def crear_autor(session: Session, autor: Autor): #el service coordina la operación y confirma los cambios
    guardar_autor(session, autor)
    session.commit()
    session.refresh(autor)
    return autor