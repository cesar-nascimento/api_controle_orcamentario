from uuid import UUID

from app.entity.models import Receita, Despesa
from app.entity.schema import (
    ReceitaResponseSchema,
    DespesaResponseSchema,
)


async def create(
    item: Receita | Despesa,
) -> ReceitaResponseSchema | DespesaResponseSchema | None:
    item_ja_existe = await item.filter(
        descricao__iexact=item.descricao,
        data__year=item.data.year,
        data__month=item.data.month,
    ).first()
    if item_ja_existe:
        return None
    await item.save()
    return item


async def get_all(
    item: Receita | Despesa,
) -> list[ReceitaResponseSchema] | list[DespesaResponseSchema]:
    return await item.all()


async def get(id: UUID, item: Receita | Despesa):
    return await item.filter(id=id).first()


async def put(
    id: UUID,
    item_novo: Receita | Despesa,
    item_antigo: ReceitaResponseSchema | DespesaResponseSchema,
    table: Receita | Despesa,
) -> ReceitaResponseSchema | DespesaResponseSchema | None:
    item_novo_ja_existe = await table.filter(
        descricao__iexact=item_novo.descricao,
        data__year=item_novo.data.year,
        data__month=item_novo.data.month,
    ).first()
    if item_novo_ja_existe and item_novo_ja_existe.id != id:
        return None
    await item_antigo.update_from_dict(item_novo.as_dict()).save()
    return item_antigo


async def delete(
    id: UUID, item: Receita | Despesa
) -> ReceitaResponseSchema | DespesaResponseSchema:
    receita = await item.filter(id=id).first().delete()
    return receita
