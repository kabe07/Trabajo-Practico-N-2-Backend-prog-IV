from sqlmodel import Session

from models.libro import Libro
from models.libro_autor import Libro_Autor


def buscar_libro_por_id(session:Session, libro_id:int):
    return session.get(Libro, libro_id)#Libro le indica a la sesión en qué tabla buscar.

def buscar_asociaciones(session: Session, libro_id: int, autor_id: int):
    return session.get(Libro_Autor,(libro_id,autor_id) )

def guardar_asociaciones(session: Session, libro_id:int,autor_id: int):
    asociacion= Libro_Autor(libro_id=libro_id, autor_id=autor_id)
    session.add(asociacion)
    return asociacion 

def guardar_libro(session:Session,libro:Libro):
    session.add(libro)
    session.flush() #Inserta una nueva fila a la tabla y obtenemos el ID
    return libro
