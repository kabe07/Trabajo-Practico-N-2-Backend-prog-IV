from sqlmodel import SQLModel, Field
from models.autor import Autor


class Libro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    isbn: str = Field(unique=True)
    stock: int = Field(default=0, ge=0)
    anio: int | None = None


class LibroCreacion(SQLModel):
    titulo: str = Field(min_length=1)
    isbn: str = Field(min_length=1)
    stock: int = Field(default=0, ge=0)
    anio: int | None = Field(default=None, ge=1)


class LibroActualizacion(SQLModel):
    titulo: str | None = Field(default=None, min_length=1)
    isbn: str | None = Field(default=None, min_length=1)
    stock: int | None = Field(default=None, ge=0)
    anio: int | None = Field(default=None, ge=1)


class LibroRespuesta(SQLModel):
    id: int
    titulo: str
    isbn: str
    stock: int
    anio: int | None
    autores: list[Autor] = Field(default_factory=list)
