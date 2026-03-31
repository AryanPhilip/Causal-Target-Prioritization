import { describe, expect, it } from "vitest";

import { isTextScalePreference, isThemePreference } from "@/lib/preferences";

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

describe("isTextScalePreference", () => {
  it("accepts normal, large, larger", () => {
    expect(isTextScalePreference("normal")).toBe(true);
    expect(isTextScalePreference("large")).toBe(true);
    expect(isTextScalePreference("larger")).toBe(true);
  });

  it("rejects other values", () => {
    expect(isTextScalePreference(null)).toBe(false);
    expect(isTextScalePreference("xl")).toBe(false);
  });
});
