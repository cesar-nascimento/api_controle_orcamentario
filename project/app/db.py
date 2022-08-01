import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

# Configuração utilizada pelo Aerich para aplicar migrações
TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=os.getenv("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
