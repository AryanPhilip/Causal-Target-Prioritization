"use client";

import { useCallback, useEffect, useLayoutEffect, useState } from "react";

import { isThemePreference, THEME_STORAGE_KEY, type ThemePreference } from "@/lib/preferences";

function effectiveThemeFromDom(): "light" | "dark" {
  if (typeof document === "undefined") {
    return "light";
  }
  const attr = document.documentElement.getAttribute("data-theme");
  if (attr === "dark") {
    return "dark";
  }
  if (attr === "light") {
    return "light";
  }
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function ThemeToggle() {
  const [preference, setPreference] = useState<ThemePreference>("system");
  const [, setEffective] = useState<"light" | "dark">("light");

  const apply = useCallback((mode: ThemePreference) => {
    setPreference(mode);
    if (mode === "system") {
      document.documentElement.removeAttribute("data-theme");
    } else {
      document.documentElement.setAttribute("data-theme", mode);
    }
    try {
      localStorage.setItem(THEME_STORAGE_KEY, mode);
    } catch {
      /* ignore */
    }
    setEffective(effectiveThemeFromDom());
  }, []);

  useLayoutEffect(() => {
    let initial: ThemePreference = "system";
    try {
      const raw = localStorage.getItem(THEME_STORAGE_KEY);
      if (isThemePreference(raw)) {
        initial = raw;
      }
    } catch {
      /* ignore */
    }
    setPreference(initial);
    if (initial === "system") {
      document.documentElement.removeAttribute("data-theme");
    } else {
      document.documentElement.setAttribute("data-theme", initial);
    }
    setEffective(effectiveThemeFromDom());
  }, []);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => {
      if (preference === "system") {
        setEffective(effectiveThemeFromDom());
      }
    };
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, [preference]);

  useEffect(() => {
    setEffective(effectiveThemeFromDom());
  }, [preference]);

  const modes: Array<{ id: ThemePreference; label: string; hint: string }> = [
    { id: "light", label: "L", hint: "Light theme" },
    { id: "dark", label: "D", hint: "Dark theme" },
    { id: "system", label: "A", hint: "Match system appearance" }
  ];

  return (
    <div
      className="inline-flex shrink-0 overflow-hidden rounded border border-border-strong bg-bg-elevated shadow-[var(--shadow-tight)]"
      role="group"
      aria-label="Color theme"
    >
      {modes.map((m) => (
        <button
          key={m.id}
          type="button"
          title={m.hint}
          aria-pressed={preference === m.id}
          aria-label={m.hint}
          onClick={() => apply(m.id)}
          className={`border-r border-border px-2 py-1.5 text-[0.65rem] font-bold uppercase tracking-wide transition-[color,background-color] duration-[420ms] ease-[cubic-bezier(0.22,1,0.36,1)] last:border-r-0 ${
            preference === m.id
              ? "bg-accent-muted text-accent"
              : "text-fg-muted hover:bg-bg-muted hover:text-fg"
          }`}
        >
          {m.label}
        </button>
      ))}
    </div>
  );
}
