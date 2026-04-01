import { describe, expect, it } from "vitest";

import { isThemePreference } from "@/lib/preferences";

describe("isThemePreference", () => {
  it("accepts light, dark, system", () => {
    expect(isThemePreference("light")).toBe(true);
    expect(isThemePreference("dark")).toBe(true);
    expect(isThemePreference("system")).toBe(true);
  });

  it("rejects other values", () => {
    expect(isThemePreference(null)).toBe(false);
    expect(isThemePreference("auto")).toBe(false);
  });
});
