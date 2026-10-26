from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
FRONTEND_STATIC_DIR = FRONTEND_DIR / "static"
PAYLOADS_FILE = BASE_DIR / "payloads.json"
HONEYPOT_BASE_URL = "http://localhost:8080"
