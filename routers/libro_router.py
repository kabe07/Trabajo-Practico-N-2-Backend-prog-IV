from fastapi import APIRouter, Depends
from sqlmodel import Session
from models.libro import LibroCreacion,LibroActualizacion


from database import obtener_session
from services.libro_service import asociar_autor_a_libro, crear_libro,obtener_libros,obtener_libro_por_id,actualizar_libro

router=APIRouter(prefix="/lbros", tags=["Libros"])

@router.post("/{id}/autores/{autor_id}", status_code=201)
def asociar_autor(
    id:int,
    autor_id:int,
    session: Session=Depends(obtener_session),
):
    return asociar_autor_a_libro(session,id,autor_id)

@router.post("/", status_code=201)
def registrar_libro(
    datos: LibroCreacion,
    session: Session = Depends(obtener_session),
):
    return crear_libro(session, datos)

@router.get("/")
def consultar_libros(
    disponibles: bool = False,
    session: Session = Depends(obtener_session),
):
    return obtener_libros(session, disponibles)

@router.get("/{id}")
def consultar_libro(
    id: int,
    session: Session = Depends(obtener_session),
):
    return obtener_libro_por_id(session, id)

@router.patch("/{id}")
def modificar_libro(
    id: int,
    datos: LibroActualizacion,
    session: Session = Depends(obtener_session),
):
    return actualizar_libro(session, id, datos)