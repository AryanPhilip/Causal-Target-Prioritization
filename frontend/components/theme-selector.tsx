"use client";

import { useCallback, useEffect, useState } from "react";

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

export function ThemeSelector() {
  const [preference, setPreference] = useState<ThemePreference>("system");
  const [effective, setEffective] = useState<"light" | "dark">("light");

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

  useEffect(() => {
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
    { id: "light", label: "Light", hint: "Light background, high-contrast text" },
    { id: "dark", label: "Dark", hint: "Dark background for low ambient light" },
    { id: "system", label: "System", hint: "Match device appearance setting" }
  ];

  return (
    <div
      className="flex flex-col gap-1.5"
      role="group"
      aria-label="Color theme: choose light, dark, or match system settings"
    >
      <span className="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-fg-subtle">
        Theme
      </span>
      <div
        className="inline-flex overflow-hidden border border-border-strong bg-bg-elevated shadow-[var(--shadow-tight)]"
        role="presentation"
      >
        {modes.map((m) => (
          <button
            key={m.id}
            type="button"
            title={m.hint}
            aria-pressed={preference === m.id}
            aria-label={`${m.label} theme. ${m.hint}`}
            onClick={() => apply(m.id)}
            className={`border-r border-border last:border-r-0 px-2.5 py-1.5 text-[0.7rem] font-semibold uppercase tracking-[0.08em] transition-[color,background-color] duration-[420ms] ease-[cubic-bezier(0.22,1,0.36,1)] sm:px-3 ${
              preference === m.id
                ? "bg-accent-muted text-accent"
                : "text-fg-muted hover:bg-bg-muted hover:text-fg"
            }`}
          >
            {m.label}
          </button>
        ))}
      </div>
      {preference === "system" ? (
        <span className="text-[0.7rem] leading-snug text-fg-subtle">
          Using {effective === "dark" ? "dark" : "light"} display from your device.
        </span>
      ) : (
        <span className="text-[0.7rem] text-fg-subtle">
          {preference === "dark" ? "Dark" : "Light"} mode locked (not following system).
        </span>
      )}
    </div>
  );
}
