from sqlmodel import SQLModel, Field

class Autor(SQLModel, table=True): #Indica que la clase representa una tabla en la base de datos.
    id: int | None= Field(default=None, primary_key=True) #El id lo genera la base de datos al guardar
    nombre: str