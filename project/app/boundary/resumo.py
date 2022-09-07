from fastapi import APIRouter, HTTPException, Depends

from app.entity.schema import ResumoSchema, UsuarioInDB
from app.controller import database
from app.controller.usuario import get_current_active_user


router = APIRouter()


@router.get("/{ano}/{mes}", status_code=200)
async def read_resumo_mensal_total(
    ano: int, mes: int, usuario: UsuarioInDB = Depends(get_current_active_user)
) -> ResumoSchema:
    """Busca resumo detalhado de determinado mês.
    Retorna 422 em caso de data inválida."""
    items = await database.get_resumo_ano_mes(ano, mes, usuario)
    if items is None:
        raise HTTPException(status_code=422, detail="Data informada inválida.")
    return items
