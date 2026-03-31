import { defineConfig } from "@playwright/test";


export default defineConfig({
  testDir: "./tests/e2e",
  use: {
    baseURL: "http://127.0.0.1:3100",
    headless: true
  },
  webServer: [
    {
      command:
        "../.venv/bin/python -m uvicorn ctpc.main:app --app-dir ../backend/src --host 127.0.0.1 --port 8010",
      cwd: __dirname,
      url: "http://127.0.0.1:8010/healthz",
      reuseExistingServer: true,
      timeout: 120_000
    },
    {
      command:
        "PATH=../.tools/node/bin:$PATH CTPC_API_BASE_URL=http://127.0.0.1:8010 ../.tools/node/bin/node ./node_modules/next/dist/bin/next dev --hostname 127.0.0.1 --port 3100",
      cwd: __dirname,
      url: "http://127.0.0.1:3100",
      reuseExistingServer: true,
      timeout: 120_000
    }
  ]
});
