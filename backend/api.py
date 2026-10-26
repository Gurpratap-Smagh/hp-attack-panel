import json
import random
from typing import Any

import httpx
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.config import HONEYPOT_BASE_URL
from backend.payloads import load_payloads
from backend.ws import WebSocketManager

router = APIRouter()
ws_manager = WebSocketManager()


@router.post("/fire-random")
async def fire_random() -> dict[str, Any]:
    payload = random.choice(load_payloads())
    method = str(payload.get("method", "GET")).upper()
    path = str(payload.get("path", "/"))
    headers = payload.get("headers", {}) or {}
    body = payload.get("body")
    body_text = json.dumps(body) if isinstance(body, (dict, list)) else ("" if body is None else str(body))

    await ws_manager.broadcast(
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


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
