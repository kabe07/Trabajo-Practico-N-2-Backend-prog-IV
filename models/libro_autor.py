from sqlmodel import SQLModel, Field

class Libro_Autor(SQLModel, table=True):
    libro_id:int =Field(foreign_key="libro.id", primary_key=True)#foreign_key="libro.id" indica que libro_id apunta al ID de un libro
    autor_id:int = Field(foreign_key="autor.id", primary_key=True)  
    #Los dos campos juntos forman la clave primaria. Por ejemplo, podés guardar los pares 
    # (1, 556) y (1, 555) para asociar dos autores al libro 1, pero el par (1, 556) solo 
    # puede aparecer una vez.