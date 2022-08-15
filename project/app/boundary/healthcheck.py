from fastapi import APIRouter


router = APIRouter()


@router.get("/healthcheck", status_code=200)
async def healthcheck() -> dict:
    """Checa se a api está respondendo."""
    return {"status": "OK"}
