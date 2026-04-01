"use client";

export function SiteFooter() {
  return (
    <footer className="mt-16 border-t border-border py-8 text-center text-sm text-fg-muted">
      <p className="max-w-2xl mx-auto leading-relaxed">
        <strong className="font-semibold text-fg">CTPC</strong> — Causal target prioritization. Press{" "}
        <kbd className="rounded-[var(--radius-lg)] border border-border-strong bg-bg-muted px-1.5 py-0.5 font-mono text-xs text-fg shadow-[var(--shadow-tight)]">
          ?
        </kbd>{" "}
        for keyboard shortcuts. Theme controls are next to Admin in the header.
      </p>
    </footer>
  );
}
