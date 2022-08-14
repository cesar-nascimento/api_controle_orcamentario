from uuid import UUID

from app.entity.schema import DespesaPayloadSchema, DespesaResponseSchema
from app.entity.models import Despesa
from app.controller import database


async def post(payload: DespesaPayloadSchema) -> Despesa:
    item = Despesa(
        descricao=payload.descricao,
        valor=payload.valor,
        data=payload.data,
    )
    return await database.create(item)


async def get_all() -> list[DespesaResponseSchema]:
    items = await database.get_all(Despesa)
    return items


async def get(id: UUID) -> DespesaResponseSchema:
    item = await database.get(id, Despesa)
    return item


async def put(
    id: UUID, payload: DespesaPayloadSchema, item_antigo: DespesaResponseSchema
) -> DespesaResponseSchema | None:
    item_updated = await database.put(
        id=id, payload=payload, item_antigo=item_antigo, table=Despesa
    )
    return item_updated


async def delete(id: UUID) -> DespesaResponseSchema:
    item = await database.delete(id, Despesa)
    return item
