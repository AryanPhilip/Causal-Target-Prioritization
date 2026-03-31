# Causal-Target-Prioritization

A scientist-facing decision platform that unifies biomedical evidence across targets, diseases, compounds, trials, and safety signals, then ranks therapeutic hypotheses using an explainable causal evidence engine.

## Frontend

The Next.js app lives in [`frontend/`](frontend/). It expects a running CTPC API (see `CTPC_API_BASE_URL` in [`frontend/lib/api.ts`](frontend/lib/api.ts); defaults probe `127.0.0.1:8010` and `8000`).

```bash
cd frontend
npm install
npm run dev
```

Then open the URL shown by Next (port 3000 unless overridden). Run unit tests with `npm test`, production build with `npm run build`. End-to-end tests (`npm run e2e`) start the API and dev server per [`frontend/playwright.config.ts`](frontend/playwright.config.ts); install browsers once with `npx playwright install chromium`.
