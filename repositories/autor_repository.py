from sqlmodel import Session, select
from models.autor import Autor


def guardar_autor(session: Session, autor: Autor):#el repository prepara el guardado
    session.add(autor)
    session.flush()
    return autor

def listar_autores(session: Session):
    consulta=select(Autor)#Select(autor) ->prepara una consulta para obtener los autores
    return session.exec(consulta).all() #La ejecuta y obtiene todos los resultados.

def buscar_autor_por_id(session: Session, autor_id: int):
    return session.get(Autor, autor_id) #Aqui le estamos indicando en que entidad buscar "Autor" y buscarlo por su id.

def eliminar_autor(session: Session, autor: Autor)-> None:
    session.delete(autor)