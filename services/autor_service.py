from sqlmodel import Session
from models.autor import Autor
from repositories.autor_repository import guardar_autor, listar_autores


def crear_autor(session: Session, autor: Autor): #el service coordina la operación y confirma los cambios
    guardar_autor(session, autor)
    session.commit()
    session.refresh(autor)
    return autor

def obtener_autores(session: Session):
    return listar_autores(session)