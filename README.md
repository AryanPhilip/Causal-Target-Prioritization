# Causal Target Prioritization Copilot

A local-first monorepo MVP for ulcerative colitis target prioritization. The backend ships canonical schemas, fixture-backed ingestion, deterministic ranking, REST and GraphQL APIs, and a thin Next.js workspace UI.

## Current implementation

The implemented milestone currently lives on branch `codex/ctpc-m1` in the worktree:

```bash
/Users/aryanphilip/Developer/Causal-Target-Prioritization/.worktrees/codex-ctpc-m1
```

## Layout

- `backend/`: FastAPI, GraphQL, SQLAlchemy models, ingest pipeline, ranking services, tests
- `frontend/`: thin Next.js app for disease workspace, target detail, compare, and admin status
- `infra/`: Docker Compose and environment examples

## One-time setup

From the worktree root:

```bash
cd /Users/aryanphilip/Developer/Causal-Target-Prioritization/.worktrees/codex-ctpc-m1
```

Python:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './backend[dev]'
```

Node.js:

If `node` is already installed on your machine, use it. If not, install a repo-local copy:

```bash
./scripts/bootstrap-node.sh
export PATH="$PWD/.tools/node/bin:$PATH"
```

Then install frontend dependencies:

```bash
cd frontend
npm install
cd ..
```

## Run the app

### 1. Start the backend

From the worktree root:

```bash
. .venv/bin/activate
uvicorn ctpc.main:app --app-dir backend/src --host 127.0.0.1 --port 8010
```

Backend URLs:

- REST docs: [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs)
- GraphQL: [http://127.0.0.1:8010/graphql](http://127.0.0.1:8010/graphql)
- Health check: [http://127.0.0.1:8010/healthz](http://127.0.0.1:8010/healthz)

### 2. Start the frontend

Open a second terminal, then from the same worktree root:

```bash
export PATH="$PWD/.tools/node/bin:$PATH"
cd frontend
CTPC_API_BASE_URL=http://127.0.0.1:8010 npm run dev
```

Frontend URL:

- App: [http://127.0.0.1:3000](http://127.0.0.1:3000)

Notes:

- The frontend can auto-discover a CTPC backend by probing `healthz`, but setting `CTPC_API_BASE_URL=http://127.0.0.1:8010` is the simplest path.
- `8010` is the verified local backend port because `8000` is commonly occupied by other apps.

## Test and verify

### Backend tests

From the worktree root:

```bash
. .venv/bin/activate
cd backend && pytest -q
```

### Frontend tests

From the worktree root:

```bash
export PATH="$PWD/.tools/node/bin:$PATH"
cd frontend
npm test
```

### Production frontend build

From the worktree root:

```bash
export PATH="$PWD/.tools/node/bin:$PATH"
cd frontend
npm run build
```

### End-to-end browser smoke test

From the worktree root:

```bash
export PATH="$PWD/.tools/node/bin:$PATH"
cd frontend
npm run e2e
```

## Smoke-test the backend manually

With the backend server running:

```bash
curl 'http://127.0.0.1:8010/healthz'
curl 'http://127.0.0.1:8010/api/v1/diseases?query=ulcerative'
curl 'http://127.0.0.1:8010/api/v1/diseases/MONDO:0005101/targets'
curl 'http://127.0.0.1:8010/api/v1/targets/ENSG00000162594?disease_id=MONDO:0005101'
curl 'http://127.0.0.1:8010/api/v1/admin/sources'
```

Expected behavior:

- `healthz` returns `{"service":"ctpc-backend","status":"ok"}`
- disease search returns ulcerative colitis
- ranked targets returns `IL23R`, `JAK1`, `TNF` in that order for the balanced profile
- target detail includes linked trials, compounds, and safety signals
- admin sources returns 4 seeded source status records

## Docker Compose

If Docker is available on your machine:

```bash
cd infra
docker compose up --build
```

This starts:

- Postgres on `5433`
- backend on `8010`
- frontend on `3100`

## Notes

- The default non-Docker backend path uses seeded in-memory/demo data.
- Docker Compose is configured for Postgres, but I did not verify it on this host because `docker` is not installed here.
