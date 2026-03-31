import Link from "next/link";

import { PageShell } from "@/components/page-shell";
import { Section } from "@/components/section";
import { fetchTargetDetail } from "@/lib/api";
import { normalizeIdentifier } from "@/lib/identifiers";
import { diseaseHref } from "@/lib/urls";

export const dynamic = "force-dynamic";

const sectionNavLink =
  "border border-border bg-bg-elevated px-3 py-1.5 text-sm font-semibold text-fg-muted shadow-[var(--shadow-tight)] transition-[color,border-color] duration-[420ms] ease-[cubic-bezier(0.22,1,0.36,1)] hover:border-accent hover:text-accent";

const detailCard = "detail-card border border-border-strong bg-bg-elevated p-5 shadow-[var(--shadow-elevated)]";

const listItem = "border border-border bg-bg-muted/60 px-4 py-3 text-sm text-fg";

export default async function TargetDetailPage({
  params,
  searchParams
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ diseaseId?: string }>;
}) {
  const { id: rawId } = await params;
  const { diseaseId: rawDiseaseId = "MONDO:0005101" } = await searchParams;
  const id = normalizeIdentifier(rawId) ?? rawId;
  const diseaseId = normalizeIdentifier(rawDiseaseId) ?? rawDiseaseId;
  const detail = await fetchTargetDetail(id, diseaseId);

  const crumbs = [
    { label: "Home", href: "/" },
    { label: "Disease", href: diseaseHref(diseaseId) },
    { label: detail.targetSymbol }
  ];

  return (
    <PageShell
      title={`${detail.targetSymbol} · target detail`}
      eyebrow={detail.scorecard.explanation.summary}
      breadcrumbs={crumbs}
      contextStrip={`Target ${id} · Disease ${diseaseId}`}
      copyActions={[
        { label: "Copy target ID", value: id },
        { label: "Copy disease ID", value: diseaseId }
      ]}
    >
      <nav
        aria-label="Page sections"
        className="mb-8 flex flex-wrap gap-2 border-b border-border pb-4 text-sm"
      >
        <a href="#scores" className={sectionNavLink}>
          Scores
        </a>
        <a href="#compounds" className={sectionNavLink}>
          Compounds
        </a>
        <a href="#trials" className={sectionNavLink}>
          Trials
        </a>
        <a href="#safety" className={sectionNavLink}>
          Safety
        </a>
      </nav>

      <div id="scores" className="mb-8 grid gap-4 scroll-mt-28 md:grid-cols-3">
        <section className={detailCard}>
          <span className="text-xs font-semibold uppercase tracking-[0.1em] text-fg-muted">Overall score</span>
          <strong className="mt-2 block font-display text-3xl font-bold tabular-nums text-fg">
            {detail.scorecard.overallScore}
          </strong>
        </section>
        <section className={detailCard}>
          <span className="text-xs font-semibold uppercase tracking-[0.1em] text-fg-muted">Confidence</span>
          <strong className="mt-2 block font-display text-3xl font-bold text-fg">
            {detail.scorecard.confidenceLabel}
          </strong>
        </section>
        <section className={detailCard}>
          <span className="text-xs font-semibold uppercase tracking-[0.1em] text-fg-muted">Percentile</span>
          <strong className="mt-2 block font-display text-3xl font-bold tabular-nums text-fg">
            {detail.scorecard.percentile}
          </strong>
        </section>
      </div>

      <div id="compounds" className="mb-8 scroll-mt-28">
        <Section title="Linked compounds" description="Chemical matter associated with this target in the seeded vertical.">
          <ul className="pill-row grid gap-2 sm:grid-cols-2">
            {detail.linkedCompounds.map((compound) => (
              <li key={compound.chemblId} className={listItem}>
                <span className="font-medium">{compound.name}</span>{" "}
                <small className="font-mono text-fg-muted">({compound.chemblId})</small>
                <div className="mt-1 text-xs text-fg-muted">Modality: {compound.modality}</div>
              </li>
            ))}
          </ul>
        </Section>
      </div>

      <div id="trials" className="mb-8 scroll-mt-28">
        <Section
          title="Clinical trials"
          description="Registry identifiers and phase for quick provenance checks."
        >
          <ul className="link-list grid gap-2">
            {detail.linkedTrials.map((trial) => (
              <li key={trial.nctId} className={listItem}>
                <Link
                  className="font-mono font-semibold text-accent underline-offset-4 hover:underline"
                  href={`https://clinicaltrials.gov/study/${trial.nctId}`}
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  {trial.nctId}
                </Link>{" "}
                <span className="text-fg">{trial.title}</span>{" "}
                <small className="tabular-nums text-fg-muted">{trial.phase}</small>
              </li>
            ))}
          </ul>
        </Section>
      </div>

      <div id="safety" className="scroll-mt-28">
        <Section title="Safety signals" description="Signals that inform the safety penalty in the ranking profile.">
          <ul className="link-list grid gap-2">
            {detail.safetySignals.map((signal) => (
              <li
                key={`${signal.source}-${signal.ingredient}`}
                className={listItem}
              >
                <strong>{signal.ingredient}</strong>{" "}
                <span className="text-fg-muted">{signal.detail}</span>
                {signal.warningFlag ? (
                  <span className="ml-2 inline-flex border border-warn/40 bg-warn/10 px-2 py-0.5 text-xs font-semibold uppercase tracking-wider text-warn shadow-[var(--shadow-tight)]">
                    Warning
                  </span>
                ) : null}
              </li>
            ))}
          </ul>
        </Section>
      </div>
    </PageShell>
  );
}
