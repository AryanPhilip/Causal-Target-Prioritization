import { describe, expect, it } from "vitest";

import { normalizeIdentifier } from "@/lib/identifiers";

describe("normalizeIdentifier", () => {
  it("decodes encoded canonical ids from route params", () => {
    expect(normalizeIdentifier("MONDO%3A0005101")).toBe("MONDO:0005101");
  });

  it("returns the original value when it is already normalized", () => {
    expect(normalizeIdentifier("ENSG00000162594")).toBe("ENSG00000162594");
  });
});
