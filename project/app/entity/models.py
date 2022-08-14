from enum import Enum

from tortoise import fields
from tortoise.models import Model


class CustomDateField(fields.DateField):
    def to_db_value(self, value: int, _) -> int:
        self.validate(value)
        return value


class Categorias(str, Enum):
    ALIMENTACAO = "Alimentação"
    SAUDE = "Saúde"
    MORADIA = "Moradia"
    TRANSPORTE = "Transporte"
    EDUCACAO = "Educação"
    LAZER = "Lazer"
    IMPREVISTOS = "Imprevistos"
    OUTRAS = "Outras"


class Receita(Model):
    id = fields.UUIDField(pk=True)
    descricao = fields.TextField(max_length=255)
    valor = fields.DecimalField(max_digits=9, decimal_places=2)
    data = CustomDateField()

    def as_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "data": self.data,
        }


class Despesa(Model):
    id = fields.UUIDField(pk=True)
    descricao = fields.TextField(max_length=255)
    valor = fields.DecimalField(max_digits=9, decimal_places=2)
    data = CustomDateField()
    categoria = fields.CharEnumField(Categorias, default=Categorias.OUTRAS)

    def as_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "data": self.data,
            "categoria": self.categoria,
        }
