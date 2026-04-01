import Link from "next/link";

import { MetricStrip } from "@/components/metric-strip";
import { PageShell } from "@/components/page-shell";
import { SourceStatusPanel } from "@/components/source-status-panel";
import { TrustStrip } from "@/components/trust-strip";
import { fetchDiseases, fetchSourceStatus } from "@/lib/api";
import { diseaseHref } from "@/lib/urls";

export const dynamic = "force-dynamic";

const DEFAULT_WORKSPACE_DISEASE = "MONDO:0005101";

export default async function HomePage() {
  const [diseases, sourceStatus] = await Promise.all([fetchDiseases(), fetchSourceStatus()]);
  const workspaceDiseaseId =
    diseases.find((d) => d.id === DEFAULT_WORKSPACE_DISEASE)?.id ??
    diseases[0]?.id ??
    DEFAULT_WORKSPACE_DISEASE;

  return (
    <PageShell
      title="Evidence, ranked."
      eyebrow="A scientist-facing workspace that unifies biomedical evidence and ranks therapeutic hypotheses with an explainable causal profile—starting with an ulcerative colitis vertical."
    >
      <section className="mb-10 grid gap-8 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
        <div className="rounded-[var(--radius-lg)] border border-border bg-bg-elevated p-6 shadow-[var(--shadow-elevated)] md:p-8">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-accent">Query workspace</p>
          <h2 className="mt-3 font-display text-2xl font-semibold tracking-tight text-fg md:text-3xl">
            Ulcerative colitis target prioritization
          </h2>
          <p className="mt-4 text-sm leading-relaxed text-fg-muted md:text-base">
            Start with a governed shortlist you can defend: association, clinical, chemical, and safety
            signals synthesized into a single transparent score—not a black box.
          </p>
          <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:items-center">
            <label className="sr-only" htmlFor="home-disease-query">
              Disease focus
            </label>
            <input
              id="home-disease-query"
              className="min-w-0 flex-1 rounded-2xl border border-border bg-bg-muted px-4 py-3 font-mono text-sm text-fg tabular-nums outline-none ring-ring/0 transition focus:border-accent focus:ring-2 focus:ring-ring"
              defaultValue="ulcerative colitis"
              readOnly
              aria-readonly
            />
            <Link
              className="inline-flex justify-center rounded-full border border-accent bg-accent px-6 py-3 text-sm font-semibold text-accent-fg shadow-sm transition hover:opacity-90"
              href={diseaseHref(workspaceDiseaseId)}
            >
              Open workspace
            </Link>
          </div>
        </div>
        <MetricStrip
          stacked
          className="mb-0"
          items={[
            { label: "Disease scope", value: "1" },
            { label: "Rankable targets", value: "3" },
            { label: "Sources online", value: `${sourceStatus.length}` }
          ]}
        />
      </section>

      <div className="mb-10">
        <TrustStrip />
      </div>

      <SourceStatusPanel items={sourceStatus} />
    </PageShell>
  );
}
