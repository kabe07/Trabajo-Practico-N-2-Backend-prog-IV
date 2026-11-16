from datetime import date, timedelta
import pytest
from sqlmodel import Session, select
from models.prestamo import Prestamo


def autor(cliente, nombre="Borges"):
    respuesta = cliente.post("/autores/", json={"nombre": nombre, "nacionalidad": "Argentina"})
    assert respuesta.status_code == 201
    return respuesta.json()


def libro(cliente, isbn="123", stock=5):
    respuesta = cliente.post("/libros/", json={
        "titulo": "Ficciones", "isbn": isbn, "stock": stock, "anio": 1944,
    })
    assert respuesta.status_code == 201
    return respuesta.json()


def socio(cliente, email="ana@example.com", activo=True):
    respuesta = cliente.post("/socios/", json={"nombre": "Ana", "email": email, "activo": activo})
    assert respuesta.status_code == 201
    return respuesta.json()


def prestar(cliente, socio_id, libro_id):
    return cliente.post("/prestamos/", json={"socio_id": socio_id, "libro_id": libro_id})


def test_crud_autores(cliente):
    assert cliente.get("/").status_code == 200
    a = autor(cliente)
    assert cliente.get("/autores/").json() == [a]
    assert cliente.get(f"/autores/{a['id']}").json() == a
    respuesta = cliente.patch(f"/autores/{a['id']}", json={"nombre": "Cortazar", "nacionalidad": "Argentina"})
    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Cortazar"
    assert cliente.delete(f"/autores/{a['id']}").status_code == 204
    assert cliente.get(f"/autores/{a['id']}").status_code == 404


def test_crud_libros_y_relaciones(cliente):
    a = autor(cliente)
    b = autor(cliente, "Otro autor")
    l = libro(cliente)
    otro = libro(cliente, "456", 0)
    for autor_id in (a["id"], b["id"]):
        assert cliente.post(f"/libros/{l['id']}/autores/{autor_id}").status_code == 201
    assert cliente.post(f"/libros/{l['id']}/autores/{a['id']}").status_code == 409
    # N-N: el mismo autor tambien puede estar en otro libro.
    assert cliente.post(f"/libros/{otro['id']}/autores/{a['id']}").status_code == 201
    detalle = cliente.get(f"/libros/{l['id']}").json()
    assert {a["id"], b["id"]} == {x["id"] for x in detalle["autores"]}
    assert detalle["anio"] == 1944
    assert len(cliente.get("/libros/").json()) == 2
    assert [x["id"] for x in cliente.get("/libros/?disponibles=true").json()] == [l["id"]]
    assert cliente.patch(f"/libros/{l['id']}", json={"titulo": "Nuevo", "stock": 2, "anio": 2000}).json()["stock"] == 2
    assert cliente.delete(f"/autores/{b['id']}").status_code == 204
    assert len(cliente.get(f"/libros/{l['id']}").json()["autores"]) == 1
    assert cliente.delete(f"/libros/{l['id']}").status_code == 204
    assert cliente.get(f"/libros/{l['id']}").status_code == 404
    assert cliente.get(f"/autores/{a['id']}").status_code == 200


def test_isbn_duplicado_crear_y_actualizar(cliente):
    l = libro(cliente)
    otro = libro(cliente, "456")
    assert cliente.post("/libros/", json={"titulo": "Otro", "isbn": l["isbn"]}).status_code == 409
    assert cliente.patch(f"/libros/{otro['id']}", json={"isbn": l["isbn"]}).status_code == 409
    assert cliente.get(f"/libros/{otro['id']}").json()["isbn"] == "456"


def test_crud_socios_email_duplicado(cliente):
    s = socio(cliente)
    otro = socio(cliente, "otro@example.com")
    assert len(cliente.get("/socios/").json()) == 2
    assert cliente.get(f"/socios/{s['id']}").json() == s
    assert cliente.post("/socios/", json={"nombre": "Duplicado", "email": s["email"]}).status_code == 409
    assert cliente.patch(f"/socios/{otro['id']}", json={"email": s["email"]}).status_code == 409
    assert cliente.get(f"/socios/{otro['id']}").json()["email"] == "otro@example.com"
    actualizado = cliente.patch(f"/socios/{s['id']}", json={"activo": False, "nombre": "Ana Maria"})
    assert actualizado.status_code == 200
    assert actualizado.json()["activo"] is False
    assert cliente.delete(f"/socios/{s['id']}").status_code == 204


def test_limite_tres_prestamos_y_devolucion_libera_cupo(cliente):
    s, l = socio(cliente), libro(cliente)
    prestamos = []
    for _ in range(3):
        respuesta = prestar(cliente, s["id"], l["id"])
        assert respuesta.status_code == 201
        prestamos.append(respuesta.json())
    assert prestar(cliente, s["id"], l["id"]).status_code == 409
    assert cliente.get(f"/libros/{l['id']}").json()["stock"] == 2
    assert len(cliente.get(f"/socios/{s['id']}/prestamos?activos=true").json()) == 3
    assert cliente.post(f"/prestamos/{prestamos[0]['id']}/devolucion").status_code == 200
    assert prestar(cliente, s["id"], l["id"]).status_code == 201
    assert len(cliente.get(f"/socios/{s['id']}/prestamos").json()) == 4
    assert len(cliente.get(f"/socios/{s['id']}/prestamos?activos=true").json()) == 3


def test_sin_stock_no_crea_prestamo(cliente):
    s, l = socio(cliente), libro(cliente, stock=0)
    assert prestar(cliente, s["id"], l["id"]).status_code == 409
    assert cliente.get(f"/socios/{s['id']}/prestamos").json() == []
    assert cliente.get(f"/libros/{l['id']}").json()["stock"] == 0


def test_socio_inactivo_no_descuenta_stock(cliente):
    s, l = socio(cliente, activo=False), libro(cliente)
    assert prestar(cliente, s["id"], l["id"]).status_code == 403
    assert cliente.get(f"/libros/{l['id']}").json()["stock"] == 5
    assert cliente.get(f"/socios/{s['id']}/prestamos").json() == []


@pytest.mark.parametrize("atraso,multa", [(-1, 0), (0, 0), (1, 100), (5, 500)])
def test_vencimiento_stock_multa_y_doble_devolucion(cliente, motor, atraso, multa):
    s, l = socio(cliente), libro(cliente)
    respuesta = prestar(cliente, s["id"], l["id"])
    assert respuesta.status_code == 201
    p = respuesta.json()
    assert p["fecha_prestamo"] == date.today().isoformat()
    assert date.fromisoformat(p["fecha_vencimiento"]) == date.fromisoformat(p["fecha_prestamo"]) + timedelta(days=14)
    assert p["multa"] == 0 and p["fecha_devolucion"] is None
    assert cliente.get(f"/libros/{l['id']}").json()["stock"] == 4
    with Session(motor) as session:
        registro = session.get(Prestamo, p["id"])
        registro.fecha_vencimiento = date.today() - timedelta(days=atraso)
        registro.fecha_prestamo = registro.fecha_vencimiento - timedelta(days=14)
        session.commit()
    devolucion = cliente.post(f"/prestamos/{p['id']}/devolucion")
    assert devolucion.status_code == 200
    assert devolucion.json()["multa"] == multa
    assert devolucion.json()["fecha_devolucion"] == date.today().isoformat()
    assert cliente.get(f"/libros/{l['id']}").json()["stock"] == 5
    assert cliente.post(f"/prestamos/{p['id']}/devolucion").status_code == 409
    assert cliente.get(f"/libros/{l['id']}").json()["stock"] == 5
    assert cliente.get(f"/socios/{s['id']}/prestamos?activos=true").json() == []


@pytest.mark.parametrize("recurso", ["autores", "libros", "socios"])
def test_recursos_inexistentes(cliente, recurso):
    assert cliente.get(f"/{recurso}/999").status_code == 404
    assert cliente.patch(f"/{recurso}/999", json={"nombre": "X", "titulo": "X"}).status_code == 404
    assert cliente.delete(f"/{recurso}/999").status_code == 404


def test_prestamos_y_asociaciones_inexistentes(cliente):
    s, l, a = socio(cliente), libro(cliente), autor(cliente)
    assert prestar(cliente, 999, l["id"]).status_code == 404
    assert prestar(cliente, s["id"], 999).status_code == 404
    assert cliente.post("/prestamos/999/devolucion").status_code == 404
    assert cliente.get("/socios/999/prestamos?activos=true").status_code == 404
    assert cliente.post(f"/libros/999/autores/{a['id']}").status_code == 404
    assert cliente.post(f"/libros/{l['id']}/autores/999").status_code == 404


@pytest.mark.parametrize("stock", [-1, -10])
def test_stock_negativo(cliente, stock):
    assert cliente.post("/libros/", json={"titulo": "X", "isbn": "X", "stock": stock}).status_code == 422
    l = libro(cliente)
    assert cliente.patch(f"/libros/{l['id']}", json={"stock": stock}).status_code == 422
    assert cliente.get(f"/libros/{l['id']}").json()["stock"] == 5


def test_no_borra_historial(cliente):
    s, l = socio(cliente), libro(cliente)
    p = prestar(cliente, s["id"], l["id"]).json()
    for _ in range(2):
        assert cliente.delete(f"/libros/{l['id']}").status_code == 409
        assert cliente.delete(f"/socios/{s['id']}").status_code == 409
        cliente.post(f"/prestamos/{p['id']}/devolucion")


def test_campos_opcionales_y_email_invalido(cliente):
    l = libro(cliente)
    assert cliente.patch(f"/libros/{l['id']}", json={"titulo": None}).json()["titulo"] == l["titulo"]
    assert cliente.post("/socios/", json={"nombre": "Ana", "email": "invalido"}).status_code == 422
    assert cliente.post("/autores/", json={"nombre": ""}).status_code == 422
