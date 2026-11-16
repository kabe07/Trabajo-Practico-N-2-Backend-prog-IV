from sqlalchemy import inspect
from sqlmodel import create_engine
import database


def test_actualiza_base_anterior_sin_perder_datos(monkeypatch):
    motor = create_engine("sqlite://")
    with motor.begin() as connection:
        connection.exec_driver_sql("CREATE TABLE autor (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL)")
        connection.exec_driver_sql("CREATE TABLE libro (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, ISBN TEXT UNIQUE NOT NULL, stock INTEGER NOT NULL)")
        connection.exec_driver_sql("INSERT INTO autor VALUES (1, 'Borges')")
        connection.exec_driver_sql("INSERT INTO libro VALUES (1, 'Ficciones', '123', 3)")
    monkeypatch.setattr(database, "engine", motor)
    database.crear_tablas()
    database.crear_tablas()
    with motor.connect() as connection:
        assert connection.exec_driver_sql("SELECT nombre, nacionalidad FROM autor").one() == ("Borges", "")
        assert connection.exec_driver_sql("SELECT titulo, isbn, stock, anio FROM libro").one() == ("Ficciones", "123", 3, None)
        assert "prestamo" in inspect(connection).get_table_names()
    motor.dispose()
