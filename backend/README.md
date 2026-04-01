# CTPC backend

FastAPI service implementing the REST contract expected by [`../frontend/lib/api.ts`](../frontend/lib/api.ts).

## Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Start Postgres (from repo root):

```bash
docker compose up -d postgres
export DATABASE_URL=postgresql+psycopg://ctpc:ctpc@127.0.0.1:5432/ctpc
alembic upgrade head
```

Run API:

```bash
uvicorn ctpc.main:app --app-dir src --host 127.0.0.1 --port 8010
```

Populate data (calls OpenTargets, ChEMBL, ClinicalTrials.gov; may take a few minutes):

```bash
curl -X POST http://127.0.0.1:8010/internal/jobs/ingest
# Optional: protect with INTERNAL_JOB_TOKEN — send header Authorization: Bearer <token>
```

Environment variables:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | SQLAlchemy URL (default local `ctpc:ctpc@127.0.0.1:5432/ctpc`) |
| `INGEST_ON_STARTUP` | Set `true` to run ingest when the process starts (slow) |
| `CTPC_DISABLE_SCHEDULER` | Set `1` to disable the 6-hour APScheduler job (tests) |
| `INTERNAL_JOB_TOKEN` | If set, `POST /internal/jobs/ingest` requires `Authorization: Bearer …` |

## Tests

```bash
CTPC_DISABLE_SCHEDULER=1 pytest
```

## Migrations

```bash
export DATABASE_URL=postgresql+psycopg://ctpc:ctpc@127.0.0.1:5432/ctpc
alembic revision --autogenerate -m "message"   # when models change
alembic upgrade head
```
