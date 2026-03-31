export const THEME_STORAGE_KEY = "ctpc-theme";
export const TEXT_SCALE_STORAGE_KEY = "ctpc-text-scale";

export type ThemePreference = "light" | "dark" | "system";
export type TextScalePreference = "normal" | "large" | "larger";

export function isThemePreference(v: string | null): v is ThemePreference {
  return v === "light" || v === "dark" || v === "system";
}

export function isTextScalePreference(v: string | null): v is TextScalePreference {
  return v === "normal" || v === "large" || v === "larger";
}
