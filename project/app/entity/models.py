from typing import Optional, Union, Type

from tortoise import fields, models
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class DateFieldNoParsing(fields.DateField):
    def to_db_value(self, value: int, instance: "Union[Type[Model], Model]"):
        self.validate(value)
        return value


class Receita(models.Model):
    id = fields.IntField(pk=True)
    descricao = fields.TextField(max_length=255)
    valor = fields.DecimalField(max_digits=9, decimal_places=2)
    data = DateFieldNoParsing()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return self.descricao


class Despesa(models.Model):
    id = fields.IntField(pk=True)
    descricao = fields.TextField(max_length=255)
    valor = fields.DecimalField(max_digits=9, decimal_places=2)
    data = DateFieldNoParsing()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return self.descricao


ReceitaSchema = pydantic_model_creator(Receita)
DespesaSchema = pydantic_model_creator(Despesa)
