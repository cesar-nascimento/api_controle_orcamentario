from uuid import UUID

from app.entity.schema import ReceitaPayloadSchema, ReceitaResponseSchema
from app.entity.models import Receita
from app.controller import database


async def post(payload: ReceitaPayloadSchema) -> Receita:
    item = Receita(
        descricao=payload.descricao,
        valor=payload.valor,
        data=payload.data,
    )
    return await database.create(item)


async def get_all(descricao: str | None) -> list[ReceitaResponseSchema]:
    items = await database.get_all(descricao, Receita)
    return items


async def get_all_ano_mes(ano: int, mes: int) -> list[ReceitaResponseSchema] | None:
    items = await database.get_all_ano_mes(ano, mes, Receita)
    return items


async def get(id: UUID) -> ReceitaResponseSchema:
    item = await database.get(id, Receita)
    return item


async def put(
    id: UUID, payload: ReceitaPayloadSchema, item_antigo: ReceitaResponseSchema
) -> ReceitaResponseSchema | None:
    item_novo = Receita(
        descricao=payload.descricao,
        valor=payload.valor,
        data=payload.data,
    )
    item_updated = await database.put(
        id=id, item_novo=item_novo, item_antigo=item_antigo, table=Receita
    )
    return item_updated


async def delete(id: UUID) -> ReceitaResponseSchema:
    item = await database.delete(id, Receita)
    return item
