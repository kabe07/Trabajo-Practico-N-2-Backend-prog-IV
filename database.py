from sqlmodel import SQLModel, create_engine
from models.autor import Autor #Permite que SQLModel conozca el modelo y su tabla


engine= create_engine("sqlite:///biblioteca.db") #Aqui indico que motor de base de datos voy a utilizar y donde se van a guardar los datos.

def crear_tablas(): #Es una funcion que crea las tablas que todavia no existen en esa base de datos.
    SQLModel.metadata.create_all(engine)