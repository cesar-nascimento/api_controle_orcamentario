from uuid import UUID

from app.entity.schema import ReceitaPayloadSchema, ReceitaResponseSchema, Usuario
from app.entity.models import Receita
from app.controller import database


async def post(payload: ReceitaPayloadSchema, usuario: Usuario) -> Receita:
    item = Receita(
        descricao=payload.descricao,
        valor=payload.valor,
        data=payload.data,
    )
    return await database.create(item, usuario)


async def get_all(
    descricao: str | None, usuario: Usuario
) -> list[ReceitaResponseSchema]:
    items = await database.get_all(descricao, Receita, usuario)
    return items


async def get_all_ano_mes(
    ano: int, mes: int, usuario: Usuario
) -> list[ReceitaResponseSchema] | None:
    items = await database.get_all_ano_mes(ano, mes, Receita, usuario)
    return items


async def get(id: UUID, usuario: Usuario) -> ReceitaResponseSchema:
    item = await database.get(id, Receita, usuario)
    return item


async def put(
    id: UUID,
    payload: ReceitaPayloadSchema,
    item_antigo: ReceitaResponseSchema,
    usuario: Usuario,
) -> ReceitaResponseSchema | None:
    item_novo = Receita(
        descricao=payload.descricao,
        valor=payload.valor,
        data=payload.data,
    )
    item_updated = await database.put(
        id=id,
        item_novo=item_novo,
        item_antigo=item_antigo,
        table=Receita,
        usuario=usuario,
    )
    return item_updated


async def delete(id: UUID, usuario: Usuario) -> ReceitaResponseSchema:
    item = await database.delete(id, Receita, usuario)
    return item
