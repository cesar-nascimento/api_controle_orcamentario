from app.entity.schema import ReceitaPayloadSchema
from app.entity.models import Receita


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
