import { afterEach, describe, expect, it, vi } from "vitest";

import { fetchDiseases, resetApiBaseUrlCache } from "@/lib/api";


describe("api base URL resolution", () => {
  afterEach(() => {
    resetApiBaseUrlCache();
    vi.restoreAllMocks();
    delete process.env.CTPC_API_BASE_URL;
  });

  it("falls back from a non-CTPC service on port 8000 to the healthy CTPC backend", async () => {
    const fetchMock = vi.fn(async (input: URL | RequestInfo) => {
      const url = String(input);

      if (url === "http://127.0.0.1:8010/healthz") {
        return new Response(JSON.stringify({ service: "ctpc-backend" }), {
          status: 200,
          headers: { "content-type": "application/json" }
        });
      }

      if (url === "http://127.0.0.1:8010/api/v1/diseases?query=ulcerative") {
        return new Response(JSON.stringify({ items: [{ id: "MONDO:0005101" }] }), {
          status: 200,
          headers: { "content-type": "application/json" }
        });
      }

      if (url === "http://127.0.0.1:8000/healthz") {
        return new Response("missing", { status: 404 });
      }

      throw new Error(`Unexpected URL ${url}`);
    });

    vi.stubGlobal("fetch", fetchMock);

    const items = await fetchDiseases();

    expect(items[0].id).toBe("MONDO:0005101");
    expect(fetchMock).toHaveBeenCalledWith("http://127.0.0.1:8010/healthz", { cache: "no-store" });
    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8010/api/v1/diseases?query=ulcerative",
      { cache: "no-store" }
    );
  });
});
