import logging

from fastapi import FastAPI

from app.db import init_db
from app.boundary import healthcheck, receitas, despesas


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:

    application = FastAPI()
    application.include_router(healthcheck.router)
    application.include_router(receitas.router, prefix="/receitas", tags=["receitas"])
    application.include_router(despesas.router, prefix="/despesas", tags=["despesas"])
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
