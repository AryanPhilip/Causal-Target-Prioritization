"use client";

import { useCallback, useState } from "react";

type CopyButtonProps = {
  text: string;
  label: string;
  /** Announcement for screen readers after copy */
  copiedLabel?: string;
};

export function CopyButton({ text, label, copiedLabel = "Copied to clipboard" }: CopyButtonProps) {
  const [status, setStatus] = useState<"idle" | "copied" | "error">("idle");

  const copy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(text);
      setStatus("copied");
      window.setTimeout(() => setStatus("idle"), 2200);
    } catch {
      setStatus("error");
      window.setTimeout(() => setStatus("idle"), 2200);
    }
  }, [text]);

  const shown = status === "copied" ? copiedLabel : status === "error" ? "Copy failed" : label;

  return (
    <button
      type="button"
      onClick={copy}
      className="inline-flex items-center gap-1.5 rounded-full border border-border bg-bg-elevated px-2.5 py-1 text-xs font-medium text-fg shadow-sm transition hover:border-accent hover:text-accent focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
    >
      <span aria-hidden className="font-mono text-[0.7rem] opacity-80">
        {status === "idle" ? "⎘" : status === "copied" ? "✓" : "!"}
      </span>
      <span aria-live="polite">{shown}</span>
    </button>
  );
}
