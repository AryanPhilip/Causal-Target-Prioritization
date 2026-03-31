export function HowRankingWorks() {
  return (
    <details className="group rounded-2xl border border-border bg-bg-muted/40 open:bg-bg-elevated">
      <summary className="cursor-pointer list-none px-4 py-3 text-sm font-medium text-accent marker:content-none [&::-webkit-details-marker]:hidden">
        <span className="inline-flex items-center gap-2">
          <span aria-hidden className="inline-block transition group-open:rotate-90">
            ▸
          </span>
          How ranking works
        </span>
      </summary>
      <div className="border-t border-border px-4 pb-4 pt-3 text-sm leading-relaxed text-fg-muted">
        <p>
          Targets receive a balanced profile score from association evidence, clinical trial support,
          chemical matter, tractability, a confidence modifier, and a safety penalty. Higher is better
          except safety, which subtracts when burden increases. Expand any row to read the narrative
          rationale tied to this disease context.
        </p>
      </div>
    </details>
  );
}
