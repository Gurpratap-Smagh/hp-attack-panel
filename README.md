# hp-attack-panel

A minimal FastAPI + vanilla JS attack trigger panel for a local honeypot.

## Requirements

- Python 3.10+
- Honeypot service running on `http://localhost:8080`

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

Open `http://localhost:5000` in your browser.

## Notes

- `POST /fire-random` picks one payload from `payloads.json` and sends it to the honeypot at `localhost:8080`.
- `WS /ws` streams the outgoing request details (`method`, `path`, `headers`, `body`) to the frontend log pane.
