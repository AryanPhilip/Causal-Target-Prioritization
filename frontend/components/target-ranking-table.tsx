import Link from "next/link";

import { ScoreBreakdown } from "@/components/score-breakdown";
import { TargetScorecard } from "@/lib/types";
import { compareHref, targetHref } from "@/lib/urls";

type TargetRankingTableProps = {
  items: TargetScorecard[];
  diseaseId?: string;
};

export function TargetRankingTable({ items, diseaseId }: TargetRankingTableProps) {
  return (
    <section
      aria-labelledby="ranked-heading"
      className="rounded-[var(--radius-lg)] border border-border bg-bg-elevated p-6 shadow-[var(--shadow-elevated)] md:p-8"
    >
      <header className="mb-6 border-b border-border pb-4">
        <h2 id="ranked-heading" className="font-display text-lg font-semibold text-fg md:text-xl">
          Ranked targets
        </h2>
        <p className="mt-2 text-sm text-fg-muted">
          Balanced profile with transparent score decomposition and visible safety penalties.
        </p>
      </header>
      <div className="grid gap-5">
        {items.map((item) => (
          <article
            className="ranking-card rounded-2xl border border-border bg-bg-muted/40 p-5 transition hover:border-border-strong md:p-6"
            key={item.targetId}
          >
            <div className="ranking-card-main flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div className="min-w-0 flex-1">
                <div className="ranking-symbol-row flex flex-wrap items-center gap-3">
                  <strong className="ranking-symbol font-mono text-lg text-fg">{item.targetSymbol}</strong>
                  <span className="inline-flex rounded-full border border-border-strong bg-bg-elevated px-3 py-1 text-[0.7rem] font-semibold uppercase tracking-wider text-fg-muted">
                    {item.confidenceLabel}
                  </span>
                </div>
                <p className="ranking-name mt-2 text-sm text-fg-muted">{item.targetName}</p>
              </div>
              <div className="ranking-score text-left sm:text-right">
                <span className="block font-display text-3xl font-semibold tabular-nums text-fg">
                  {item.overallScore}
                </span>
                <small className="text-xs text-fg-muted">{item.percentile}th percentile</small>
              </div>
            </div>

            <div className="mt-6 border-t border-border pt-5">
              <ScoreBreakdown components={item.components} />
            </div>

            <details className="explanation-drawer group mt-5 rounded-xl border border-border bg-bg-elevated open:border-accent/40">
              <summary className="cursor-pointer list-none px-4 py-3 text-sm font-medium text-accent marker:content-none [&::-webkit-details-marker]:hidden">
                <span className="inline-flex items-center gap-2">
                  <span aria-hidden className="inline-block transition group-open:rotate-90">
                    ▸
                  </span>
                  Why this rank
                </span>
              </summary>
              <div className="border-t border-border px-4 pb-4 pt-3 text-sm leading-relaxed text-fg-muted">
                {item.explanation.summary}
              </div>
            </details>

            <div className="card-actions mt-4 flex flex-wrap gap-3">
              <Link
                href={targetHref(item.targetId, diseaseId ?? item.diseaseId)}
                className="inline-flex rounded-full border border-border bg-bg-elevated px-4 py-2 text-sm font-medium text-fg transition hover:border-accent hover:text-accent"
              >
                Target detail
              </Link>
              <Link
                href={compareHref(diseaseId ?? item.diseaseId, [item.targetId])}
                className="inline-flex rounded-full border border-border bg-transparent px-4 py-2 text-sm font-medium text-fg-muted transition hover:border-border-strong hover:text-fg"
              >
                Compare
              </Link>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
