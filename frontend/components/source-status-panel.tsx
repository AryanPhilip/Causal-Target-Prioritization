import { SourceStatus } from "@/lib/types";

type SourceStatusPanelProps = {
  items: SourceStatus[];
};

function badgeClass(status: string): string {
  const s = status.toLowerCase();
  if (s.includes("warn") || s.includes("degraded")) {
    return "border-warn/35 bg-warn/10 text-warn";
  }
  if (s.includes("fail") || s.includes("error")) {
    return "border-danger/35 bg-danger/10 text-danger";
  }
  return "border-accent/30 bg-accent-muted text-accent";
}

export function SourceStatusPanel({ items }: SourceStatusPanelProps) {
  return (
    <section
      aria-labelledby="source-status-heading"
      className="rounded-[var(--radius-lg)] border border-border bg-bg-elevated p-6 shadow-[var(--shadow-elevated)] md:p-8"
    >
      <header className="mb-6 border-b border-border pb-4">
        <h2 id="source-status-heading" className="font-display text-lg font-semibold text-fg md:text-xl">
          System health &amp; ingest status
        </h2>
        <p className="mt-2 text-sm text-fg-muted">
          Freshness, row counts, and validation state for connected evidence sources. Use this panel
          to confirm pipelines before interpreting rankings.
        </p>
      </header>
      <div className="grid gap-4 md:grid-cols-2">
        {items.map((item) => (
          <article
            key={item.source}
            className="rounded-2xl border border-border bg-bg-muted/50 p-5 transition hover:border-border-strong"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <strong className="font-mono text-sm text-fg">{item.source}</strong>
              <span
                className={`inline-flex min-w-[4.5rem] justify-center rounded-full border px-2.5 py-1 text-[0.7rem] font-semibold uppercase tracking-wider ${badgeClass(item.validationStatus)}`}
              >
                {item.validationStatus}
              </span>
            </div>
            <dl className="mt-4 grid gap-3 text-sm">
              <div className="flex justify-between gap-4">
                <dt className="text-fg-muted">Freshness</dt>
                <dd className="tabular-nums text-fg">{item.freshnessHours}h</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-fg-muted">Rows</dt>
                <dd className="tabular-nums text-fg">{item.rowCount}</dd>
              </div>
              <div className="flex justify-between gap-4">
                <dt className="text-fg-muted">Mapping coverage</dt>
                <dd className="tabular-nums text-fg">{Math.round(item.mappingCoverage * 100)}%</dd>
              </div>
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}
