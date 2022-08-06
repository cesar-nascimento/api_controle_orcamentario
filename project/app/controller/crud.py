from app.entity.schema import ReceitaPayloadSchema, ReceitaResponseSchema
from app.entity.models import Receita
from fastapi import HTTPException


async def post(payload: ReceitaPayloadSchema) -> int:
    receita = Receita(
        descricao=payload.descricao,
        valor=payload.valor,
        data=payload.data,
    )
    receita_ja_existe = (
        await Receita.filter(data=receita.data)
        .filter(descricao=receita.descricao)
        .first()
    )
    if receita_ja_existe:
        return None
    await receita.save()
    return receita.id


async def get_all() -> list[ReceitaResponseSchema]:
    receitas = await Receita.all().values()
    return receitas


async def get(id: int) -> ReceitaResponseSchema:
    receita = await Receita.filter(id=id).first().values()
    if not receita:
        return None
    return receita


async def put(id: int, payload: ReceitaPayloadSchema) -> dict | None:
    receita = await Receita.filter(id=id).first()
    if not receita:
        return None
    receita_ja_existe = (
        await Receita.filter(data=payload.data)
        .filter(descricao=payload.descricao)
        .first()
    )
    if receita_ja_existe and receita_ja_existe.id != receita.id:
        raise HTTPException(
            status_code=409,
            detail="Update vai gerar descrição duplicada para o mês informado.",
        )
    await Receita.filter(id=id).update(
        data=payload.data, valor=payload.valor, descricao=payload.descricao
    )
    updated_receita = await Receita.filter(id=id).first().values()
    return updated_receita
