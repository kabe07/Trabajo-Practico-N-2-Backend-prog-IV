from sqlmodel import Session
from models.autor import Autor


def guardar_autor(session: Session, autor: Autor):#el repository prepara el guardado
    session.add(autor)
    session.flush()
    return autor