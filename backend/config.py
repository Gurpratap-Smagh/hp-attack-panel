from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PAYLOADS_FILE = BASE_DIR / "payloads.json"
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"
HONEYPOT_BASE_URL = "http://localhost:8080"
