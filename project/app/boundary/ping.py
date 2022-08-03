from fastapi import APIRouter


router = APIRouter()


@router.get("/healthcheck", status_code=200)
async def healthcheck() -> dict:
    return {"status": "OK"}
