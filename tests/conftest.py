import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine
import database
from main import app


@pytest.fixture
def motor(monkeypatch):
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    @event.listens_for(engine, "connect")
    def claves(connection, record):
        connection.execute("PRAGMA foreign_keys=ON")
    monkeypatch.setattr(database, "engine", engine)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def cliente(motor):
    with TestClient(app) as client:
        yield client
