from decimal import Decimal
from datetime import date

from pydantic import BaseModel


class ReceitaPayloadSchema(BaseModel):
    descricao: str
    valor: Decimal
    data: date


class ReceitaResponseSchema(ReceitaPayloadSchema):
    id: int


class DespesaPayloadSchema(BaseModel):
    descricao: str
    valor: Decimal
    data: date


class DespesaResponseSchema(DespesaPayloadSchema):
    id: int
