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
      const isHelpKey =
        e.key === "?" || (e.key === "/" && e.shiftKey) || (e.code === "Slash" && e.shiftKey);
      if (isHelpKey && !e.ctrlKey && !e.metaKey && !e.altKey) {
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

  const kbd =
    "shrink-0 rounded-[var(--radius-lg)] border border-border-strong bg-bg-muted px-2 py-1 font-mono text-xs text-fg shadow-[var(--shadow-tight)]";

  return (
    <div
      className="fixed inset-0 z-[100] flex items-end justify-center p-4 sm:items-center"
      role="presentation"
    >
      <button
        type="button"
        className="absolute inset-0 bg-bg/85 backdrop-blur-sm"
        aria-label="Close shortcuts"
        onClick={close}
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="kbd-title"
        className="ds-panel relative z-[101] w-full max-w-md border-border-strong p-6"
      >
        <h2 id="kbd-title" className="font-display text-lg font-bold text-fg">
          Keyboard shortcuts
        </h2>
        <p className="mt-2 text-sm text-fg-muted">
          Press <kbd className={kbd}>?</kbd> anywhere (outside text fields) to toggle this panel.
        </p>
        <ul className="mt-4 space-y-3 text-sm text-fg">
          <li className="flex justify-between gap-4 border-b border-border pb-2">
            <span className="text-fg-muted">Toggle this help</span>
            <kbd className={kbd}>?</kbd>
          </li>
          <li className="flex justify-between gap-4 border-b border-border pb-2">
            <span className="text-fg-muted">Close dialog</span>
            <kbd className={kbd}>Esc</kbd>
          </li>
          <li className="flex justify-between gap-4">
            <span className="text-fg-muted">Dismiss (click backdrop)</span>
            <span className="text-fg-subtle text-xs">Click outside</span>
          </li>
        </ul>
        <button
          type="button"
          onClick={close}
          className="ds-link-cta mt-6 w-full border-border-strong py-2.5 text-sm normal-case tracking-normal"
        >
          Close
        </button>
      </div>
    </div>
  );
}
