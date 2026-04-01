# Causal-Target-Prioritization

A scientist-facing decision platform that unifies biomedical evidence across targets, diseases, compounds, trials, and safety signals, then ranks therapeutic hypotheses using an explainable causal evidence engine.

## Repository layout

| Path | Role |
|------|------|
| [`frontend/`](frontend/) | Next.js UI (reads API from `CTPC_API_BASE_URL`) |
| [`backend/`](backend/) | FastAPI + Postgres + scheduled ingest (OpenTargets, ChEMBL, ClinicalTrials.gov) |
| [`docker-compose.yml`](docker-compose.yml) | Local Postgres 16 for development |

## Quick start (local)

1. **Database**

   ```bash
   docker compose up -d postgres
   ```

2. **Backend** — see [`backend/README.md`](backend/README.md): create a venv, `pip install -e ".[dev]"`, `alembic upgrade head`, run `uvicorn`, then `POST /internal/jobs/ingest` to load public data.

3. **Frontend**

   ```bash
   cd frontend
   npm install
   export CTPC_API_BASE_URL=http://127.0.0.1:8010
   npm run dev
   ```

   Open the URL printed by Next (port 3000 by default).

4. **Tests**

   - Frontend: `cd frontend && npm test` and `npm run build`
   - Backend: `cd backend && CTPC_DISABLE_SCHEDULER=1 pytest`

## Deployment (free-tier friendly)

- **Frontend:** Vercel (or similar) — set `CTPC_API_BASE_URL` to your public API URL.
- **API:** Render / Railway / Fly.io — run `uvicorn ctpc.main:app` with `DATABASE_URL` pointing to managed Postgres.
- **Database:** Neon or Supabase Postgres — use their connection string as `DATABASE_URL`.
- **Cron:** Call `POST /internal/jobs/ingest` on a schedule (GitHub Actions, Render cron, etc.) with `Authorization: Bearer …` if `INTERNAL_JOB_TOKEN` is set.

## End-to-end tests

Playwright config lives in [`frontend/playwright.config.ts`](frontend/playwright.config.ts). It expects Postgres migrated, the API on port **8010**, and data ingested (`POST /internal/jobs/ingest`) before `npm run e2e`. With `reuseExistingServer: true`, you can start the API and Next manually, then run e2e.

Install browsers once: `cd frontend && npx playwright install chromium`.
