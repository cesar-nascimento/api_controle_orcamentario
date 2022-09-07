from uuid import UUID

from app.entity.schema import DespesaPayloadSchema, DespesaResponseSchema, UsuarioInDB
from app.entity.models import Despesa
from app.controller import database


async def post(payload: DespesaPayloadSchema, usuario: UsuarioInDB) -> Despesa:
    item = Despesa(
        descricao=payload.descricao,
        valor=payload.valor,
        data=payload.data,
        categoria=payload.categoria,
        usuario_id=usuario.id,
    )
    return await database.create(item, usuario)


async def get_all(
    descricao: str | None, usuario: UsuarioInDB
) -> list[DespesaResponseSchema]:
    items = await database.get_all(descricao, Despesa, usuario)
    return items


async def get_all_ano_mes(
    ano: int, mes: int, usuario: UsuarioInDB
) -> list[DespesaResponseSchema] | None:
    items = await database.get_all_ano_mes(ano, mes, Despesa, usuario)
    return items


async def get(id: UUID, usuario: UsuarioInDB) -> DespesaResponseSchema:
    item = await database.get(id, Despesa, usuario)
    return item


async def put(
    id: UUID,
    payload: DespesaPayloadSchema,
    item_antigo: DespesaResponseSchema,
    usuario: UsuarioInDB,
) -> DespesaResponseSchema | None:
    item_novo = Despesa(
        descricao=payload.descricao,
        valor=payload.valor,
        data=payload.data,
        categoria=payload.categoria,
        usuario_id=usuario.id,
    )
    item_updated = await database.put(
        id=id, item_novo=item_novo, item_antigo=item_antigo, table=Despesa, user=usuario
    )
    return item_updated


async def delete(id: UUID, usuario: UsuarioInDB) -> DespesaResponseSchema:
    item = await database.delete(id, Despesa, usuario)
    return item
