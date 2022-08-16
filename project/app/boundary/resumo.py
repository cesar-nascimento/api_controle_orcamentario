from fastapi import APIRouter, HTTPException
from app.entity.schema import ResumoSchema
from app.controller import database


router = APIRouter()


@router.get("/{ano}/{mes}", status_code=200)
async def read_resumo_mensal_total(ano: int, mes: int) -> ResumoSchema:
    """Busca resumo detalhado de determinado mês.
    Retorna 422 em caso de data inválida."""
    items = await database.get_resumo_ano_mes(ano, mes)
    if items is None:
        raise HTTPException(status_code=422, detail="Data informada inválida.")
    return items
