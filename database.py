from sqlmodel import SQLModel, Session, create_engine
from models.autor import Autor #Permite que SQLModel conozca el modelo y su tabla


engine= create_engine("sqlite:///biblioteca.db", connect_args={"check_same_thread":False},) #Aqui indico que motor de base de datos voy a utilizar y donde se van a guardar los datos.
#check_same_thread=False permite usar SQLite con los distintos hilos con los que FastAPI puede atender peticiones.

def crear_tablas(): #Es una funcion que crea las tablas que todavia no existen en esa base de datos.
    SQLModel.metadata.create_all(engine)

def obtener_session():
    with Session(engine) as session:#crea una sesión usando nuestra conexión.
        yield session #entrega esa sesión al endpoint que la necesite.