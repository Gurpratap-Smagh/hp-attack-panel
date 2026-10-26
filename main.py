import json
import random
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
PAYLOADS_FILE = BASE_DIR / "payloads.json"
HONEYPOT_BASE_URL = "http://localhost:8080"

app = FastAPI(title="hp-attack-panel")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

connected_clients: set[WebSocket] = set()


def load_payloads() -> list[dict[str, Any]]:
    with PAYLOADS_FILE.open("r", encoding="utf-8") as f:
        payloads = json.load(f)
    if not isinstance(payloads, list) or not payloads:
        raise ValueError("payloads.json must contain a non-empty list")
    return payloads


async def broadcast_request_details(payload: dict[str, Any]) -> None:
    details = {
        "method": payload.get("method", "GET"),
        "path": payload.get("path", "/"),
        "headers": payload.get("headers", {}),
        "body": payload.get("body"),
    }
    stale_clients = []
    for client in connected_clients:
        try:
            await client.send_json(details)
        except Exception:
            stale_clients.append(client)

    for client in stale_clients:
        connected_clients.discard(client)


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/fire-random")
async def fire_random() -> dict[str, Any]:
    payload = random.choice(load_payloads())
    method = str(payload.get("method", "GET")).upper()
    path = str(payload.get("path", "/"))
    headers = payload.get("headers", {}) or {}
    body = payload.get("body")
    body_text = json.dumps(body) if isinstance(body, (dict, list)) else ("" if body is None else str(body))

    await broadcast_request_details(
        {
            "method": method,
            "path": path,
            "headers": headers,
            "body": body_text,
        }
    )

    url = f"{HONEYPOT_BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.request(method=method, url=url, headers=headers, content=body_text)

    return {
        "payload_id": payload.get("id"),
        "payload_name": payload.get("name"),
        "target_url": url,
        "status_code": response.status_code,
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.discard(websocket)
