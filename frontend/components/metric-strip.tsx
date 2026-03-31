type MetricStripProps = {
  items: Array<{ label: string; value: string }>;
  /** Single column (e.g. beside hero on home) */
  stacked?: boolean;
  className?: string;
};

export function MetricStrip({ items, stacked, className = "mb-8" }: MetricStripProps) {
  const grid = stacked ? "grid-cols-1" : "sm:grid-cols-2 lg:grid-cols-3";
  return (
    <div className={`grid gap-4 ${grid} ${className}`}>
      {items.map((item) => (
        <article key={item.label} className="ds-panel border-border-strong p-5">
          <span className="text-xs font-semibold uppercase tracking-[0.1em] text-fg-muted">
            {item.label}
          </span>
          <strong className="mt-2 block font-display text-2xl font-bold tabular-nums text-fg">
            {item.value}
          </strong>
        </article>
      ))}
    </div>
  );
}
