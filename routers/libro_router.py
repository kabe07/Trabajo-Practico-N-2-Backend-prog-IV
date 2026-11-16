from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import obtener_session
from models.libro import LibroCreacion, LibroActualizacion, LibroRespuesta
from services.libro_service import (
    asociar_autor_a_libro, crear_libro, obtener_libros,
    obtener_libro_por_id, actualizar_libro, borrar_libro, respuesta_libro,
)

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post("/{id}/autores/{autor_id}", status_code=201)
def asociar_autor(id: int, autor_id: int, session: Session = Depends(obtener_session)):
    return asociar_autor_a_libro(session, id, autor_id)


@router.post("/", status_code=201, response_model=LibroRespuesta)
def registrar_libro(datos: LibroCreacion, session: Session = Depends(obtener_session)):
    return crear_libro(session, datos)


@router.get("/", response_model=list[LibroRespuesta])
def consultar_libros(disponibles: bool = False, session: Session = Depends(obtener_session)):
    return obtener_libros(session, disponibles)


@router.get("/{id}", response_model=LibroRespuesta)
def consultar_libro(id: int, session: Session = Depends(obtener_session)):
    return respuesta_libro(session, obtener_libro_por_id(session, id))


@router.patch("/{id}", response_model=LibroRespuesta)
def modificar_libro(id: int, datos: LibroActualizacion, session: Session = Depends(obtener_session)):
    return actualizar_libro(session, id, datos)


@router.delete("/{id}", status_code=204)
def eliminar_libro(id: int, session: Session = Depends(obtener_session)) -> None:
    borrar_libro(session, id)
