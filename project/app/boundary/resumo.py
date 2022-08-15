from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from app.entity.schema import ReceitaPayloadSchema, ReceitaResponseSchema
from app.controller import database


router = APIRouter()


@router.get("/{ano}/{mes}", status_code=200)
async def read_resumo_ano_mes(ano: int, mes: int) -> list[ReceitaResponseSchema]:
    """Busca resumo detalhado de determinado mês.
    Retorna 422 em caso de data inválida."""
    items = await database.get_resumo_ano_mes(ano, mes)
    if items is None:
        raise HTTPException(status_code=422, detail="Data informada inválida.")
    return items
