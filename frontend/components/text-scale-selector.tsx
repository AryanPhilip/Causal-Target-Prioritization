"use client";

import { useCallback, useEffect, useState } from "react";

import {
  isTextScalePreference,
  TEXT_SCALE_STORAGE_KEY,
  type TextScalePreference
} from "@/lib/preferences";

export function TextScaleSelector() {
  const [scale, setScale] = useState<TextScalePreference>("normal");

  const apply = useCallback((next: TextScalePreference) => {
    setScale(next);
    if (next === "normal") {
      document.documentElement.removeAttribute("data-text-scale");
    } else {
      document.documentElement.setAttribute("data-text-scale", next);
    }
    try {
      localStorage.setItem(TEXT_SCALE_STORAGE_KEY, next);
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    let initial: TextScalePreference = "normal";
    try {
      const raw = localStorage.getItem(TEXT_SCALE_STORAGE_KEY);
      if (isTextScalePreference(raw)) {
        initial = raw;
      }
    } catch {
      /* ignore */
    }
    setScale(initial);
    if (initial === "normal") {
      document.documentElement.removeAttribute("data-text-scale");
    } else {
      document.documentElement.setAttribute("data-text-scale", initial);
    }
  }, []);

  const options: Array<{ id: TextScalePreference; label: string; hint: string }> = [
    { id: "normal", label: "Default", hint: "Standard text size" },
    { id: "large", label: "Large", hint: "Slightly larger body text" },
    { id: "larger", label: "Larger", hint: "Extra-large for readability" }
  ];

  return (
    <div
      className="flex flex-col gap-1.5"
      role="group"
      aria-label="Text size for the whole app"
    >
      <span className="text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-fg-subtle">
        Text size
      </span>
      <div className="inline-flex flex-wrap rounded-full border border-border bg-bg-muted/80 p-0.5 shadow-sm">
        {options.map((o) => (
          <button
            key={o.id}
            type="button"
            title={o.hint}
            aria-pressed={scale === o.id}
            aria-label={`${o.label} text. ${o.hint}`}
            onClick={() => apply(o.id)}
            className={`rounded-full px-2 py-1.5 text-xs font-semibold transition sm:px-2.5 ${
              scale === o.id
                ? "bg-bg-elevated text-fg shadow-sm ring-1 ring-border-strong"
                : "text-fg-muted hover:text-fg"
            }`}
          >
            {o.label}
          </button>
        ))}
      </div>
    </div>
  );
}
