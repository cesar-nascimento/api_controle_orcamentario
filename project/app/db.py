import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

from app.entity.models import Usuario
from app.controller import usuario


# Configuração utilizada pelo Aerich para aplicar migrações
TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.entity.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.getenv("DATABASE_URL"),
        modules={"models": ["app.entity.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def criar_usuarios_fake(db_url=None):
    # Atenção.
    # Usuarios criados apenas para exemplo e demonstração da API.
    # Não criar dessa forma se estiver clonando o projeto do Github.
    fake_users_db = [
        {
            "username": "garibaldo",
            "password": "admin",
            "disabled": False,
        },
        {
            "username": "elmo",
            "password": "admin",
            "disabled": True,
        },
    ]
    if not db_url:
        db_url = os.getenv("DATABASE_URL")
    await Tortoise.init(db_url=db_url, modules={"models": ["app.entity.models"]})
    await Tortoise.generate_schemas()
    for user in fake_users_db:
        item = Usuario(
            username=user["username"],
            password=user["password"],
            disabled=user["disabled"],
        )
        await usuario.create_usuario(item)
    await Tortoise.close_connections()
