import Link from "next/link";

import { ScoreBreakdown } from "@/components/score-breakdown";
import { TargetScorecard } from "@/lib/types";
import { compareHref, targetHref } from "@/lib/urls";

type TargetRankingTableProps = {
  items: TargetScorecard[];
  diseaseId?: string;
};

const badgeBase =
  "inline-flex min-h-[1.5rem] items-center border border-border-strong bg-bg-elevated px-2 py-0.5 text-[0.65rem] font-semibold uppercase tracking-[0.12em] text-fg-muted shadow-[var(--shadow-tight)]";

const linkPrimary = "ds-link-cta text-sm normal-case tracking-normal";
const linkGhost =
  "inline-flex items-center justify-center border border-border bg-transparent px-4 py-2 text-sm font-semibold text-fg-muted shadow-[var(--shadow-tight)] transition-[color,border-color] duration-[420ms] ease-[cubic-bezier(0.22,1,0.36,1)] hover:border-border-strong hover:text-fg";

export function TargetRankingTable({ items, diseaseId }: TargetRankingTableProps) {
  return (
    <section aria-labelledby="ranked-heading" className="ds-panel border-border-strong p-6 md:p-8">
      <header className="mb-6 border-b border-border pb-4">
        <h2 id="ranked-heading" className="font-display text-lg font-bold text-fg md:text-xl">
          Ranked targets
        </h2>
        <p className="mt-2 text-sm text-fg-muted">
          Balanced profile with transparent score decomposition and visible safety penalties.
        </p>
      </header>
      <div className="grid gap-5">
        {items.map((item) => (
          <article
            className="ranking-card border border-border bg-bg-muted/35 p-5 transition-[border-color] duration-[420ms] ease-[cubic-bezier(0.22,1,0.36,1)] hover:border-border-strong md:p-6"
            key={item.targetId}
          >
            <div className="ranking-card-main flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div className="min-w-0 flex-1">
                <div className="ranking-symbol-row flex flex-wrap items-center gap-3">
                  <strong className="ranking-symbol font-mono text-lg text-fg">{item.targetSymbol}</strong>
                  <span className={badgeBase}>{item.confidenceLabel}</span>
                </div>
                <p className="ranking-name mt-2 text-sm text-fg-muted">{item.targetName}</p>
              </div>
              <div className="ranking-score text-left sm:text-right">
                <span className="block font-display text-3xl font-bold tabular-nums text-fg">
                  {item.overallScore}
                </span>
                <small className="text-xs text-fg-muted">{item.percentile}th percentile</small>
              </div>
            </div>

            <div className="mt-6 border-t border-border pt-5">
              <ScoreBreakdown components={item.components} />
            </div>

            <details className="explanation-drawer group mt-5 border border-border bg-bg-elevated open:border-accent/50">
              <summary className="cursor-pointer list-none px-4 py-3 text-sm font-semibold text-accent marker:content-none [&::-webkit-details-marker]:hidden">
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
              <Link href={targetHref(item.targetId, diseaseId ?? item.diseaseId)} className={linkPrimary}>
                Target detail
              </Link>
              <Link href={compareHref(diseaseId ?? item.diseaseId, [item.targetId])} className={linkGhost}>
                Compare
              </Link>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
