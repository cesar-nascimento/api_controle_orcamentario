from enum import Enum

from tortoise import fields
from tortoise.models import Model


class CustomDateField(fields.DateField):
    def to_db_value(self, value: int, _) -> int:
        self.validate(value)
        return value


class Receita(Model):
    id = fields.UUIDField(pk=True)
    descricao = fields.TextField(max_length=255)
    valor = fields.DecimalField(max_digits=9, decimal_places=2)
    data = CustomDateField()


class Despesa(Model):
    id = fields.UUIDField(pk=True)
    descricao = fields.TextField(max_length=255)
    valor = fields.DecimalField(max_digits=9, decimal_places=2)
    data = CustomDateField()
