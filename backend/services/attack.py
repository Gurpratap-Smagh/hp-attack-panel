import json
import random
from typing import Any

import httpx

from backend.config import HONEYPOT_BASE_URL
from backend.services.payloads import load_payloads
from backend.services.realtime import broadcast_request_details


async def fire_random_payload() -> dict[str, Any]:
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
