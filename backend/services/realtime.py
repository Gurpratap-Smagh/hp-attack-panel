from typing import Any

from fastapi import WebSocket

connected_clients: set[WebSocket] = set()


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
