from pydantic import Field as CampoValidado
from sqlmodel import SQLModel, Field


class Socio(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(unique=True)
    activo: bool = True


class SocioCreacion(SQLModel):
    nombre: str = Field(min_length=1)
    email: str = CampoValidado(pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    activo: bool = True


class SocioActualizacion(SQLModel):
    nombre: str | None = Field(default=None, min_length=1)
    email: str | None = CampoValidado(default=None, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    activo: bool | None = None

