from sqlmodel import Session, select

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

def listar_libros(session: Session, disponibles: bool = False):
    consulta = select(Libro)

    if disponibles:
        consulta = consulta.where(Libro.stock > 0)

    return session.exec(consulta).all()




def obtener_autores_libro(session: Session, libro_id: int):
    from models.autor import Autor
    consulta = select(Autor).join(
        Libro_Autor, Libro_Autor.autor_id == Autor.id
    ).where(Libro_Autor.libro_id == libro_id)
    return session.exec(consulta).all()


def eliminar_libro(session: Session, libro: Libro):
    asociaciones = session.exec(
        select(Libro_Autor).where(Libro_Autor.libro_id == libro.id)
    ).all()
    for asociacion in asociaciones:
        session.delete(asociacion)
    session.flush()
    session.delete(libro)
