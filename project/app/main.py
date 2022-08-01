import logging

from fastapi import FastAPI, Depends

from app.db import init_db


log = logging.getLogger("uvicorn")


app = FastAPI()


@app.get("/ping")
def pong():
    return {"ping": "pong"}


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
