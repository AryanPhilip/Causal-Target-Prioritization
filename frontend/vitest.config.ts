import path from "node:path";

import { defineConfig } from "vitest/config";

export default defineConfig({
  esbuild: {
    jsx: "automatic",
    jsxImportSource: "react"
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname)
    }
  },
  test: {
    exclude: [
      "**/.*/**",
      "**/coverage/**",
      "**/dist/**",
      "**/node_modules/**",
      ".next/**",
      "tests/e2e/**",
      "playwright.config.ts"
    ],
    environment: "jsdom",
    globals: true,
    setupFiles: ["./vitest.setup.ts"]
  }
});
