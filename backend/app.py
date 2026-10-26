from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.api import router
from backend.config import FRONTEND_DIST_DIR

app = FastAPI(title="hp-attack-panel")
app.include_router(router)

if FRONTEND_DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST_DIR / "assets"), name="assets")


@app.get("/")
async def index() -> FileResponse | JSONResponse:
    index_file = FRONTEND_DIST_DIR / "index.html"
    if not index_file.exists():
        return JSONResponse(
            status_code=503,
            content={
                "error": "Frontend build not found.",
                "hint": "Run `npm install && npm run build` inside frontend/.",
            },
        )
    return FileResponse(index_file)
