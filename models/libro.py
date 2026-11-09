from sqlmodel import SQLModel, Field

class Libro(SQLModel, table=True):#Libro Hereda de SQLModel
    id: int | None = Field(default=None, primary_key=True)  #Puede ser entero o estar sin asignar(int | None)  Luego indica que el campo por defecto es none y que es la clave primaria
    titulo:str
    ISBN: str=Field(unique=True)
    stock:int =Field(default= 0)