from fastapi import APIRouter, HTTPException
from app.api import crud
from app.models.pydantic import ReceitaPayloadSchema, ReceitaResponseSchema


router = APIRouter()


@router.post("/", response_model=ReceitaResponseSchema, status_code=201)
async def create_receita(payload: ReceitaPayloadSchema) -> ReceitaResponseSchema:
    receita_id = await crud.post(payload)

    if not receita_id:
        raise HTTPException(
            status_code=409, detail="Descrição duplicada para o mês informado"
        )
    response_object = {
        "id": receita_id,
        "descricao": payload.descricao,
        "valor": payload.valor,
        "data": payload.data,
    }
    return response_object
