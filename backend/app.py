from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.config import FRONTEND_STATIC_DIR
from backend.routes.http import router as http_router
from backend.routes.ws import router as ws_router

app = FastAPI(title="hp-attack-panel")
app.mount("/static", StaticFiles(directory=FRONTEND_STATIC_DIR), name="static")
app.include_router(http_router)
app.include_router(ws_router)
