from datetime import date
from uuid import UUID

from pydantic import BaseModel
from pydantic import condecimal

from app.entity.models import Categorias


class BasePayloadSchema(BaseModel):
    descricao: str
    valor: condecimal(gt=0, max_digits=9, decimal_places=2)
    data: date


class BaseResponseSchema(BasePayloadSchema):
    id: UUID

    class Config:
        orm_mode = True


class ReceitaPayloadSchema(BasePayloadSchema):
    pass


class ReceitaResponseSchema(BaseResponseSchema):
    pass


class DespesaPayloadSchema(BasePayloadSchema):
    pass


class DespesaResponseSchema(BaseResponseSchema):
    pass
