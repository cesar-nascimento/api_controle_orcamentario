from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Depends


from app.controller import receita
from app.controller.usuario import get_current_active_user
from app.entity.schema import ReceitaPayloadSchema, ReceitaResponseSchema, Usuario


router = APIRouter()


@router.post("/", response_model=ReceitaResponseSchema, status_code=201)
async def create_receita(
    payload: ReceitaPayloadSchema,
    usuario: Usuario = Depends(get_current_active_user),
) -> ReceitaResponseSchema:
    """Cria uma nova receita no banco de dados ou retorna 409 em caso de duplicidade.
    Não podem existir duas receitas no mesmo mês com a mesma descrição."""
    item = await receita.post(payload, usuario)
    if not item:
        raise HTTPException(
            status_code=409, detail="Descrição duplicada para o mês informado."
        )
    return item


@router.get("/", response_model=list[ReceitaResponseSchema], status_code=200)
async def read_receitas_totais(
    descricao: str | None = Query(default=None, max_length=255),
    usuario: Usuario = Depends(get_current_active_user),
) -> list[ReceitaResponseSchema]:
    """Busca todas as receitas existentes no banco de dados.
    Aceita filtrar por descrição."""
    return await receita.get_all(descricao, usuario)


@router.get("/{id}", response_model=ReceitaResponseSchema, status_code=200)
async def read_receita(
    id: UUID, usuario: Usuario = Depends(get_current_active_user)
) -> ReceitaResponseSchema:
    """Retorna uma única receita ou 404 caso não exista receita com o id informado."""
    item = await receita.get(id, usuario)
    if not item:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    return item


@router.get("/{ano}/{mes}", response_model=list[ReceitaResponseSchema], status_code=200)
async def read_resumo_receitas_mensais(
    ano: int, mes: int, usuario: Usuario = Depends(get_current_active_user)
) -> list[ReceitaResponseSchema]:
    """Busca todas as receitas existentes no mês e ano informados.
    Retorna 422 em caso de data inválida."""
    items = await receita.get_all_ano_mes(ano, mes, usuario)
    if items is None:
        raise HTTPException(status_code=422, detail="Data informada inválida.")
    return items


@router.put("/{id}", response_model=ReceitaResponseSchema)
async def update_receita(
    id: UUID,
    payload: ReceitaPayloadSchema,
    usuario: Usuario = Depends(get_current_active_user),
) -> ReceitaResponseSchema:
    """Update de receita por id informado. Retorna 404 caso não encontrada.
    Retorna 409 caso update venha a gerar receita duplicada."""
    item = await receita.get(id, usuario)
    if not item:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    item_updated = await receita.put(
        id=id, payload=payload, item_antigo=item, usuario=usuario
    )
    if not item_updated:
        raise HTTPException(
            status_code=409,
            detail="Update vai gerar descrição duplicada para o mês informado.",
        )
    return item_updated


@router.delete("/{id}", response_model=ReceitaResponseSchema)
async def delete_receita(
    id: UUID, usuario: Usuario = Depends(get_current_active_user)
) -> ReceitaResponseSchema:
    item = await receita.get(id, usuario)
    if not item:
        raise HTTPException(status_code=404, detail="Receita não encontrada.")
    await receita.delete(id, usuario)
    return item
