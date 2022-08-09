from app.entity.schema import DespesaPayloadSchema, DespesaResponseSchema
from app.entity.models import Despesa
from fastapi import HTTPException


async def post(payload: DespesaPayloadSchema) -> int:
    despesa = Despesa(
        descricao=payload.descricao,
        valor=payload.valor,
        data=payload.data,
    )
    despesa_ja_existe = await Despesa.filter(
        descricao__iexact=despesa.descricao,
        data__year=despesa.data.year,
        data__month=despesa.data.month,
    ).first()
    if despesa_ja_existe:
        return None
    await despesa.save()
    return despesa.id


async def get_all() -> list[DespesaResponseSchema]:
    despesas = await Despesa.all().values()
    return despesas


async def get(id: int) -> DespesaResponseSchema:
    despesa = await Despesa.filter(id=id).first().values()
    if not despesa:
        return None
    return despesa


async def put(id: int, payload: DespesaPayloadSchema) -> DespesaResponseSchema | None:
    despesa = await Despesa.filter(id=id).first()
    if not despesa:
        return None
    despesa_ja_existe = await Despesa.filter(
        descricao__iexact=payload.descricao,
        data__year=payload.data.year,
        data__month=payload.data.month,
    ).first()
    if despesa_ja_existe and despesa_ja_existe.id != despesa.id:
        raise HTTPException(
            status_code=409,
            detail="Update vai gerar descrição duplicada para o mês informado.",
        )
    await Despesa.filter(id=id).update(
        data=payload.data, valor=payload.valor, descricao=payload.descricao
    )
    updated_despesa = await Despesa.filter(id=id).first().values()
    return updated_despesa


async def delete(id: int) -> DespesaResponseSchema:
    despesa = await Despesa.filter(id=id).first().delete()
    return despesa
