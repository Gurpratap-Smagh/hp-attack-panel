from fastapi import APIRouter
from fastapi.responses import FileResponse

from backend.config import FRONTEND_DIR
from backend.services.attack import fire_random_payload

router = APIRouter()


@router.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@router.post("/fire-random")
async def fire_random() -> dict:
    return await fire_random_payload()
