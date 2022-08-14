from uuid import UUID

from fastapi import APIRouter, HTTPException
from app.controller import receita
from app.entity.schema import ReceitaPayloadSchema, ReceitaResponseSchema


router = APIRouter()


@router.post("/", response_model=ReceitaResponseSchema, status_code=201)
async def create_receita(payload: ReceitaPayloadSchema) -> ReceitaResponseSchema:
    """Cria uma nova receita no banco de dados ou retorna 409 em caso de duplicidade.
    Não podem existir duas receitas no mesmo mês com a mesma descrição."""
    item = await receita.post(payload)
    if not item:
        raise HTTPException(
            status_code=409, detail="Descrição duplicada para o mês informado."
        )
    return item


@router.get("/", response_model=list[ReceitaResponseSchema], status_code=200)
async def read_all_receitas() -> list[ReceitaResponseSchema]:
    """Busca todas as receitas existentes no banco de dados."""
    return await receita.get_all()


@router.get("/{id}", response_model=ReceitaResponseSchema, status_code=200)
async def read_receita(id: UUID) -> ReceitaResponseSchema:
    """Retorna uma única receita ou 404 caso não exista receita com o id informado."""
    item = await receita.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    return item


@router.put("/{id}", response_model=ReceitaResponseSchema)
async def update_receita(
    id: UUID, payload: ReceitaPayloadSchema
) -> ReceitaResponseSchema:
    """Update de receita por id informado. Retorna 404 caso não encontrada.
    Retorna 409 caso update venha a gerar receita duplicada."""
    item = await receita.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    item_updated = await receita.put(id=id, payload=payload, item_antigo=item)
    if not item_updated:
        raise HTTPException(
            status_code=409,
            detail="Update vai gerar descrição duplicada para o mês informado.",
        )
    return item_updated


@router.delete("/{id}", response_model=ReceitaResponseSchema)
async def delete_receita(id: UUID) -> ReceitaResponseSchema:
    item = await receita.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    await receita.delete(id)
    return item
