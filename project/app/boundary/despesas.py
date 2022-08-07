from fastapi import APIRouter, HTTPException
from app.controller import crud_despesa
from app.entity.schema import DespesaPayloadSchema, DespesaResponseSchema


router = APIRouter()


@router.post("/", response_model=DespesaResponseSchema, status_code=201)
async def create_despesa(payload: DespesaPayloadSchema) -> DespesaResponseSchema:
    despesa_id = await crud_despesa.post(payload)

    if not despesa_id:
        raise HTTPException(
            status_code=409, detail="Descrição duplicada para o mês informado."
        )
    response_object = {
        "id": despesa_id,
        "descricao": payload.descricao,
        "valor": payload.valor,
        "data": payload.data,
    }
    return response_object


@router.get("/", response_model=list[DespesaResponseSchema], status_code=200)
async def read_all_despesas() -> list[DespesaResponseSchema]:
    return await crud_despesa.get_all()


@router.get("/{id}", response_model=DespesaResponseSchema, status_code=200)
async def read_despesa(id: int) -> DespesaResponseSchema:
    despesa = await crud_despesa.get(id)
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada.")

    return despesa


@router.put("/{id}", response_model=DespesaResponseSchema)
async def update_despesa(
    id: int, payload: DespesaPayloadSchema
) -> DespesaResponseSchema:
    despesa = await crud_despesa.put(id, payload)
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada.")
    return despesa


@router.delete("/{id}", response_model=DespesaResponseSchema)
async def delete_despesa(id: int) -> DespesaResponseSchema:
    despesa = await crud_despesa.get(id)
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada.")
    await crud_despesa.delete(id)
    return despesa
