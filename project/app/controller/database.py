from uuid import UUID
from datetime import date

from app.entity.models import Receita, Despesa, Categorias
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
    descricao: str | None,
    table: Receita | Despesa,
) -> list[ReceitaResponseSchema] | list[DespesaResponseSchema]:
    if descricao:
        return await table.filter(descricao__icontains=descricao)
    return await table.all()


async def get_all_ano_mes(
    ano: int,
    mes: int,
    table: Receita | Despesa,
) -> list[ReceitaResponseSchema] | list[DespesaResponseSchema] | None:
    try:
        data = date(ano, mes, 1)
    except (ValueError, OverflowError):
        return None
    return await table.filter(
        data__year=data.year,
        data__month=data.month,
    )


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


async def get_resumo_ano_mes(
    ano: int,
    mes: int,
):
    try:
        data = date(ano, mes, 1)
    except (ValueError, OverflowError):
        return None
    receitas = await Receita.filter(
        data__year=data.year,
        data__month=data.month,
    )
    despesas = await Despesa.filter(
        data__year=data.year,
        data__month=data.month,
    )
    total_receitas = sum([receita.valor for receita in receitas])
    total_despesas = sum([despesa.valor for despesa in despesas])
    saldo_final_mes = total_receitas - total_despesas
    total_despesas_por_categoria = {
        cat.value: sum(
            [despesa.valor for despesa in despesas if despesa.categoria == cat.value]
        )
        for cat in Categorias
    }
    resumo = {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo_final_mes": saldo_final_mes,
        "total_despesas_por_categoria": total_despesas_por_categoria,
    }
    return resumo
