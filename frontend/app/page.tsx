import { MetricStrip } from "@/components/metric-strip";
import { DiseaseSearch } from "@/components/disease-search";
import { PageShell } from "@/components/page-shell";
import { SourceStatusPanel } from "@/components/source-status-panel";
import { TrustStrip } from "@/components/trust-strip";
import { fetchDiseases, fetchSourceStatus } from "@/lib/api";

export const dynamic = "force-dynamic";

const DEFAULT_WORKSPACE_DISEASE = "MONDO:0005101";

export default async function HomePage() {
  const [diseases, sourceStatus] = await Promise.all([fetchDiseases(), fetchSourceStatus()]);
  const defaultDisease =
    diseases.find((d) => d.id === DEFAULT_WORKSPACE_DISEASE) ?? diseases[0];

  return (
    <PageShell
      title="Evidence, ranked."
      eyebrow="A scientist-facing workspace that unifies biomedical evidence and ranks therapeutic hypotheses with an explainable causal profile—starting with an ulcerative colitis vertical."
    >
      <section className="mb-10 grid gap-8 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
        <div className="ds-panel border-border-strong p-6 md:p-8">
          <div className="flex items-center gap-3">
            <span className="h-0.5 w-8 shrink-0 bg-accent" aria-hidden />
            <p className="text-[0.65rem] font-semibold uppercase tracking-[0.2em] text-accent">Query workspace</p>
          </div>
          <h2 className="mt-4 font-display text-2xl font-bold tracking-tight text-fg md:text-3xl">
            Search diseases &amp; open a workspace
          </h2>
          <p className="mt-4 text-sm leading-relaxed text-fg-muted md:text-base">
            Start with a governed shortlist you can defend: association, clinical, chemical, and safety
            signals synthesized into a single transparent score—not a black box.
          </p>
          <DiseaseSearch initialItems={diseases} initialQuery="ulcerative" />
        </div>
        <MetricStrip
          stacked
          className="mb-0"
          items={[
            { label: "Spotlight disease", value: defaultDisease?.label ?? "—" },
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
