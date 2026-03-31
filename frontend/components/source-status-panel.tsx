import { SourceStatus } from "@/lib/types";

type SourceStatusPanelProps = {
  items: SourceStatus[];
};

function badgeClass(status: string): string {
  const s = status.toLowerCase();
  if (s.includes("warn") || s.includes("degraded")) {
    return "border-warn/40 bg-warn/10 text-warn";
  }
  if (s.includes("fail") || s.includes("error")) {
    return "border-danger/40 bg-danger/10 text-danger";
  }
  return "border-accent/40 bg-accent-muted text-accent";
}

const statusBadge =
  "inline-flex min-w-[4.5rem] justify-center border px-2 py-1 text-[0.65rem] font-semibold uppercase tracking-[0.12em] shadow-[var(--shadow-tight)]";

export function SourceStatusPanel({ items }: SourceStatusPanelProps) {
  return (
    <section aria-labelledby="source-status-heading" className="ds-panel border-border-strong p-6 md:p-8">
      <header className="mb-6 border-b border-border pb-4">
        <h2 id="source-status-heading" className="font-display text-lg font-bold text-fg md:text-xl">
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
            className="border border-border bg-bg-muted/40 p-5 transition-[border-color] duration-[420ms] ease-[cubic-bezier(0.22,1,0.36,1)] hover:border-border-strong"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <strong className="font-mono text-sm text-fg">{item.source}</strong>
              <span className={`${statusBadge} ${badgeClass(item.validationStatus)}`}>
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
