from datetime import date
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, condecimal, SecretStr, Field

from app.entity.models import Categorias


class BasePayloadSchema(BaseModel):
    descricao: str
    valor: condecimal(gt=0, max_digits=9, decimal_places=2)
    data: date


class BaseResponseSchema(BasePayloadSchema):
    usuario = UUID
    id: UUID

    class Config:
        orm_mode = True


class ReceitaPayloadSchema(BasePayloadSchema):
    pass


class ReceitaResponseSchema(BaseResponseSchema):
    pass


class DespesaPayloadSchema(BasePayloadSchema):
    categoria: Categorias = Categorias.OUTRAS


class DespesaResponseSchema(BaseResponseSchema):
    categoria: Categorias = Categorias.OUTRAS


class ResumoSchema(BaseModel):
    total_receitas: Decimal
    total_despesas: Decimal
    saldo_final_mes: Decimal
    total_despesas_por_categoria: dict[Categorias, Decimal]


class Usuario(BaseModel):
    username: str
    disabled: bool
    password: SecretStr = Field(..., exclude=True)


class UsuarioInDB(Usuario):
    id: UUID

    class Config:
        orm_mode = True
