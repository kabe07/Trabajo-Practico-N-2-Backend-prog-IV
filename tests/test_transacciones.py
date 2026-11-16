from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
import pytest
from sqlalchemy import event
from sqlmodel import SQLModel, Session, create_engine, select
from fastapi import HTTPException
from models.libro import Libro
from models.socio import Socio
from models.prestamo import Prestamo, PrestamoCreacion
from services.prestamo_service import registrar_prestamo, registrar_devolucion
import services.prestamo_service as servicio


def test_error_al_guardar_no_descuenta_stock(motor, monkeypatch):
    with Session(motor) as session:
        session.add(Socio(id=1, nombre="Ana", email="ana@example.com"))
        session.add(Libro(id=1, titulo="X", isbn="123", stock=1))
        session.commit()
    def fallar(*args):
        raise RuntimeError("Fallo de guardado")
    monkeypatch.setattr(servicio, "guardar_prestamo", fallar)
    with Session(motor) as session:
        with pytest.raises(RuntimeError):
            registrar_prestamo(session, PrestamoCreacion(socio_id=1, libro_id=1))
    with Session(motor) as session:
        assert session.get(Libro, 1).stock == 1
        assert session.exec(select(Prestamo)).all() == []


def test_prestamos_y_devoluciones_simultaneos(tmp_path):
    motor = create_engine(
        f"sqlite:///{(tmp_path / 'concurrencia.db').as_posix()}",
        connect_args={"check_same_thread": False, "timeout": 10},
    )
    @event.listens_for(motor, "connect")
    def claves(connection, record):
        connection.execute("PRAGMA foreign_keys=ON")
    SQLModel.metadata.create_all(motor)
    with Session(motor) as session:
        session.add(Socio(id=1, nombre="Ana", email="ana@example.com"))
        session.add(Libro(id=1, titulo="X", isbn="123", stock=1))
        session.commit()
    def prestar(_):
        with Session(motor) as session:
            try:
                return 201, registrar_prestamo(session, PrestamoCreacion(socio_id=1, libro_id=1)).id
            except HTTPException as error:
                return error.status_code, None
    with ThreadPoolExecutor(max_workers=2) as pool:
        resultados = list(pool.map(prestar, range(2)))
    assert sorted(codigo for codigo, _ in resultados) == [201, 409]
    prestamo_id = next(id for codigo, id in resultados if codigo == 201)
    def devolver(_):
        with Session(motor) as session:
            try:
                registrar_devolucion(session, prestamo_id)
                return 200
            except HTTPException as error:
                return error.status_code
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(devolver, range(2))) == [200, 409]
    with Session(motor) as session:
        assert session.get(Libro, 1).stock == 1
        assert len(session.exec(select(Prestamo)).all()) == 1
    motor.dispose()
