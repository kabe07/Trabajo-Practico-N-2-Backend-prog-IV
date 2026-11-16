from datetime import date
from sqlmodel import SQLModel, Field


class Prestamo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    socio_id: int = Field(foreign_key="socio.id", index=True)
    libro_id: int = Field(foreign_key="libro.id", index=True)
    fecha_prestamo: date
    fecha_vencimiento: date
    fecha_devolucion: date | None = None
    multa: int = Field(default=0, ge=0)


class PrestamoCreacion(SQLModel):
    socio_id: int
    libro_id: int
