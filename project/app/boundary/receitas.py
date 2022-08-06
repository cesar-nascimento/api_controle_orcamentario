from fastapi import APIRouter, HTTPException
from app.controller import crud
from app.entity.schema import ReceitaPayloadSchema, ReceitaResponseSchema


router = APIRouter()


@router.post("/", response_model=ReceitaResponseSchema, status_code=201)
async def create_receita(payload: ReceitaPayloadSchema) -> ReceitaResponseSchema:
    receita_id = await crud.post(payload)

    if not receita_id:
        raise HTTPException(
            status_code=409, detail="Descrição duplicada para o mês informado."
        )
    response_object = {
        "id": receita_id,
        "descricao": payload.descricao,
        "valor": payload.valor,
        "data": payload.data,
    }
    return response_object


@router.get("/", response_model=list[ReceitaResponseSchema], status_code=200)
async def read_all_receitas() -> list[ReceitaResponseSchema]:
    return await crud.get_all()


@router.get("/{id}", response_model=ReceitaResponseSchema, status_code=200)
async def read_receita(id: int) -> ReceitaResponseSchema:
    receita = await crud.get(id)
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")

    return receita


@router.put("/{id}", response_model=ReceitaResponseSchema)
async def update_receita(
    id: int, payload: ReceitaPayloadSchema
) -> ReceitaResponseSchema:
    receita = await crud.put(id, payload)
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    return receita
