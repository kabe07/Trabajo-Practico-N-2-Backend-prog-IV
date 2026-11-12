from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import obtener_session
from services.libro_service import asociar_autor_a_libro

router=APIRouter(prefix="/lbros", tags=["Libros"])

@router.post("/{id}/autores/{autor_id}", status_code=201)
def asociar_autor(
    id:int,
    autor_id:int,
    session: Session=Depends(obtener_session),
):
    return asociar_autor_a_libro(session,id,autor_id)