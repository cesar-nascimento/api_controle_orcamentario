from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/ping")
async def pong():
    return {
        "ping": "pong!",
    }
