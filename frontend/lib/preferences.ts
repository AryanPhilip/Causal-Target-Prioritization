export const THEME_STORAGE_KEY = "ctpc-theme";

export type ThemePreference = "light" | "dark" | "system";

export function isThemePreference(v: string | null): v is ThemePreference {
  return v === "light" || v === "dark" || v === "system";
}
