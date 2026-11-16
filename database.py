from pathlib import Path
from sqlalchemy import event, inspect
from sqlmodel import SQLModel, Session, create_engine

from models.autor import Autor
from models.libro import Libro
from models.libro_autor import Libro_Autor
from models.socio import Socio
from models.prestamo import Prestamo


BASE_DIR = Path(__file__).resolve().parent
engine = create_engine(
    f"sqlite:///{(BASE_DIR / 'biblioteca.db').as_posix()}",
    connect_args={"check_same_thread": False, "timeout": 30},
)


@event.listens_for(engine, "connect")
def activar_claves_foraneas(connection, record):
    connection.execute("PRAGMA foreign_keys=ON")


def crear_tablas():
    SQLModel.metadata.create_all(engine)
    # Completa las tablas de la primera version sin borrar sus registros.
    with engine.begin() as connection:
        inspector = inspect(connection)
        columnas_autor = {c["name"].lower() for c in inspector.get_columns("autor")}
        if "nacionalidad" not in columnas_autor:
            connection.exec_driver_sql(
                "ALTER TABLE autor ADD COLUMN nacionalidad TEXT NOT NULL DEFAULT ''"
            )
        columnas_libro = {c["name"].lower() for c in inspector.get_columns("libro")}
        if "anio" not in columnas_libro:
            connection.exec_driver_sql("ALTER TABLE libro ADD COLUMN anio INTEGER")


def obtener_session():
    with Session(engine) as session:
        yield session
