# Focus-track

Simple Flask-based MVP for tracking "card" selections and user entries (minimal analytics + scheduler-ready architecture).

**What it is**
- Lightweight Flask app that stores cards and entries (timestamped) in SQLite.
- Minimal REST endpoints to add/list cards and submit entries.
- Designed as an MVP that can be extended with scheduling, analytics, and a frontend.

**Quick Summary**
- Backend: `Flask` (entrypoint: `mainrun.py`)
- ORM: `Flask-SQLAlchemy` (models in `models.py`)
- DB (dev): SQLite at `instance/selections.db`
- Routes: defined in `routecards.py`
- Dependencies: listed in `requirements.txt`
- Docker: `Dockerfile`, `docker-compose.dev.yml`, `docker-compose.prod.yml`

**Getting Started (Local)**
- Ensure Python 3.10+ is installed.
- Create the instance directory (SQLite DB file is created there):
  - `mkdir -p instance`
- Create and activate a venv:
  - `python -m venv .venv`
  - `source .venv/bin/activate`
- Install dependencies:
  - `pip install -r requirements.txt`
- Run the app:
  - `python mainrun.py`
- Access locally at: `http://127.0.0.1:5000` (API endpoints only)

**Run with Flask CLI (optional)**
- Set environment variable and run:
  - `export FLASK_APP=mainrun.py`
  - `flask run --host=0.0.0.0 --port=5000`

**Run with Docker (dev)**
- Build and run (example):
  - `docker build -t focus-track .`
  - `docker run -p 5000:5000 -v $(pwd)/instance:/app/instance focus-track`
- Or use `docker-compose.dev.yml`:
  - `docker compose -f docker-compose.dev.yml up --build`

**Environment & Files**
- `instance/` is ignored by git (contains DB and local env files).
- Put secrets (if any) into `.env` (ignored).
- DB path used by app: `sqlite:///<instance>/selections.db`

**API Reference**
All endpoints return/expect JSON.

- `POST /add_card`
  - Request body: `{ "name": "<card name>" }`
  - Success (201): `{ "message": "sucessfully added the new card", "card_id": <id> }`
  - Already exists (200): `{ "error": "Card already exists", "card_id": <id> }`
  - Error (400): `{ "error": "Card name is required" }`

- `GET /cards`
  - Response (200): `[{ "card_id": <id>, "card_name": "<name>" }, ...]`

- `POST /add_entry`
  - Request body: `{ "card_id": <card_id>, "input_text": "<optional text>" }`
  - Errors:
    - 400: `{ "error": "u must choose a card" }` (missing card_id)
    - 404: `{ "error": "card not found" }` (invalid card_id)
  - Success (201): 
    ```json
    {
      "message": "good to know u completed a task sucessfully by doing <input_text>",
      "entry_id": <id>,
      "card_name": "<name>",
      "input_text": "<input_text>"
    }
    ```

**Data model (brief)**
- `card` (table)
  - `card_id` : integer PK
  - `card_name` : string (unique, not null)
- `entries` (table)
  - `id` : integer PK
  - `card_id` : FK -> `card.card_id`
  - `input_text` : string (optional)
  - `timestamp` : datetime (defaults to UTC now)

**Examples (curl)**
- Add a card:
  - `curl -X POST -H "Content-Type: application/json" -d '{"name":"Reading"}' http://127.0.0.1:5000/add_card`
- List cards:
  - `curl http://127.0.0.1:5000/cards`
- Add an entry:
  - `curl -X POST -H "Content-Type: application/json" -d '{"card_id":1,"input_text":"30m"}' http://127.0.0.1:5000/add_entry`

**Notes & Troubleshooting**
- Ensure `instance/` exists before starting; app uses `instance/selections.db`.
- If DB tables are missing, `mainrun.py` creates them on startup via `db.create_all()` inside the app context.
- If you see import errors, confirm your virtualenv and `requirements.txt` are installed.
- `mainrun.py` sets `app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False` to avoid warnings.

**Development Ideas / Next Steps**
- Add a simple frontend (Bootstrap + fetch) to interact with the endpoints.
- Add analytics endpoints (aggregations via pandas).
- Introduce APScheduler/Celery for scheduled tasks/notifications.
- Add tests for routes and DB models.
- Add migrations (Alembic/Flask-Migrate) if evolving schema.

**Useful files**
- `mainrun.py` — app entrypoint / app factory-ish (registers blueprint + creates DB)
- `routecards.py` — API routes / blueprint (`/add_card`, `/add_entry`, `/cards`)
- `models.py` — SQLAlchemy models (`card`, `entries`)
- `requirements.txt` — Python dependencies
- `Dockerfile`, `docker-compose.dev.yml`, `docker-compose.prod.yml` — containerization

**License**
- Add a license file (e.g., `LICENSE`) if you plan to open-source.
