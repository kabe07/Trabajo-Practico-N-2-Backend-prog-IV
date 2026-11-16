from sqlmodel import SQLModel, Field

class Libro(SQLModel, table=True):#Libro Hereda de SQLModel
    id: int | None = Field(default=None, primary_key=True)  #Puede ser entero o estar sin asignar(int | None)  Luego indica que el campo por defecto es none y que es la clave primaria
    titulo:str
    isbn: str=Field(unique=True)
    stock:int =Field(default= 0)


class LibroCreacion(SQLModel):
    titulo:str
    isbn:str
    stock:int=Field(default=0, ge=0)# ge exige que sea mayor o igual a 0

class LibroActualizacion(SQLModel):
    titulo: str | None = None
    isbn: str | None = None
    stock: int | None = Field(default=None, ge=0)


