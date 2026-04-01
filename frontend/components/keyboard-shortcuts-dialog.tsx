"use client";

import { useCallback, useEffect, useState } from "react";

export function KeyboardShortcutsDialog() {
  const [open, setOpen] = useState(false);

  const close = useCallback(() => setOpen(false), []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target;
      if (
        target instanceof HTMLInputElement ||
        target instanceof HTMLTextAreaElement ||
        (target instanceof HTMLElement && target.isContentEditable)
      ) {
        return;
      }
      if (e.key === "?" && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        setOpen((v) => !v);
      }
      if (e.key === "Escape") {
        setOpen(false);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  if (!open) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-[100] flex items-end justify-center p-4 sm:items-center"
      role="presentation"
    >
      <button
        type="button"
        className="absolute inset-0 bg-bg/80 backdrop-blur-sm"
        aria-label="Close shortcuts"
        onClick={close}
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="kbd-title"
        className="relative z-[101] w-full max-w-md rounded-2xl border border-border bg-bg-elevated p-6 shadow-[var(--shadow-elevated)]"
      >
        <h2 id="kbd-title" className="font-display text-lg font-semibold text-fg">
          Keyboard shortcuts
        </h2>
        <p className="mt-2 text-sm text-fg-muted">
          Press <kbd className="rounded border border-border bg-bg-muted px-1.5 py-0.5 font-mono text-xs">?</kbd>{" "}
          anywhere (outside text fields) to toggle this panel.
        </p>
        <ul className="mt-4 space-y-3 text-sm text-fg">
          <li className="flex justify-between gap-4 border-b border-border pb-2">
            <span className="text-fg-muted">Toggle this help</span>
            <kbd className="shrink-0 rounded border border-border bg-bg-muted px-2 py-1 font-mono text-xs">
              ?
            </kbd>
          </li>
          <li className="flex justify-between gap-4 border-b border-border pb-2">
            <span className="text-fg-muted">Close dialog</span>
            <kbd className="shrink-0 rounded border border-border bg-bg-muted px-2 py-1 font-mono text-xs">
              Esc
            </kbd>
          </li>
          <li className="flex justify-between gap-4">
            <span className="text-fg-muted">Dismiss (click backdrop)</span>
            <span className="text-fg-subtle text-xs">Click outside</span>
          </li>
        </ul>
        <button
          type="button"
          onClick={close}
          className="mt-6 w-full rounded-full border border-border bg-bg-muted py-2.5 text-sm font-semibold text-fg transition hover:border-accent hover:text-accent"
        >
          Close
        </button>
      </div>
    </div>
  );
}
