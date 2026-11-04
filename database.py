from sqlmodel import create_engine
from models.autor import Autor


engine= create_engine("sqlite:///biblioteca.db") #Aqui indico que motor de base de datos voy a utilizar y donde se van a guardar los datos.

def crear_tablas():
    SQLModel.metadata.create_all(engine)