import logging

from fastapi import FastAPI

from app.db import init_db
from app.boundary import healthcheck, receitas, despesas, resumo


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    description = """
API para controle orçamentário.

Permite operações de CRUD para Receitas e Despesas.

[Github](https://github.com/cesar-nascimento/api_controle_orcamentario)
"""

    application = FastAPI(
        title="Controle Orçamentario", description=description, version="0.1.0"
    )
    application.include_router(healthcheck.router)
    application.include_router(receitas.router, prefix="/receitas", tags=["receitas"])
    application.include_router(despesas.router, prefix="/despesas", tags=["despesas"])
    application.include_router(resumo.router, prefix="/resumo", tags=["resumo"])
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
