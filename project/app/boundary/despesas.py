from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from app.controller import despesa
from app.entity.schema import DespesaPayloadSchema, DespesaResponseSchema


router = APIRouter()


@router.post("/", response_model=DespesaResponseSchema, status_code=201)
async def create_despesa(payload: DespesaPayloadSchema) -> DespesaResponseSchema:
    """Cria uma nova despesa no banco de dados ou retorna 409 em caso de duplicidade.
    Não podem existir duas despesas no mesmo mês com a mesma descrição."""
    item = await despesa.post(payload)
    if not item:
        raise HTTPException(
            status_code=409, detail="Descrição duplicada para o mês informado."
        )
    return item


@router.get("/", response_model=list[DespesaResponseSchema], status_code=200)
async def read_all_despesas(
    descricao: str | None = Query(default=None, max_length=255)
) -> list[DespesaResponseSchema]:
    """Busca todas as despesas existentes no banco de dados."""
    return await despesa.get_all(descricao)


@router.get("/{id}", response_model=DespesaResponseSchema, status_code=200)
async def read_despesa(id: UUID) -> DespesaResponseSchema:
    """Retorna uma única despesa ou 404 caso não exista despesa com o id informado."""
    item = await despesa.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Despesa não encontrada.")
    return item


@router.get("/{ano}/{mes}", response_model=list[DespesaResponseSchema], status_code=200)
async def read_all_despesas_ano_mes(ano: int, mes: int) -> list[DespesaResponseSchema]:
    """Busca todas as despesas existentes no mês e ano informados.
    Retorna 422 em caso de data inválida."""
    items = await despesa.get_all_ano_mes(ano, mes)
    if items is None:
        raise HTTPException(status_code=422, detail="Data informada inválida.")
    return items


@router.put("/{id}", response_model=DespesaResponseSchema)
async def update_despesa(
    id: UUID, payload: DespesaPayloadSchema
) -> DespesaResponseSchema:
    """Update de despesa por id informado. Retorna 404 caso não encontrada.
    Retorna 409 caso update venha a gerar despesa duplicada."""
    item = await despesa.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Despesa não encontrada.")
    item_updated = await despesa.put(id=id, payload=payload, item_antigo=item)
    if not item_updated:
        raise HTTPException(
            status_code=409,
            detail="Update vai gerar descrição duplicada para o mês informado.",
        )
    return item_updated


@router.delete("/{id}", response_model=DespesaResponseSchema)
async def delete_despesa(id: UUID) -> DespesaResponseSchema:
    item = await despesa.get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Despesa não encontrada.")
    await despesa.delete(id)
    return item
