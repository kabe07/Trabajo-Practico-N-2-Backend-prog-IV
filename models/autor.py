from sqlmodel import SQLModel, Field


class Autor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    nacionalidad: str = ""


class AutorCreacion(SQLModel):
    nombre: str = Field(min_length=1)
    nacionalidad: str = ""


class AutorActualizacion(SQLModel):
    nombre: str | None = Field(default=None, min_length=1)
    nacionalidad: str | None = None
