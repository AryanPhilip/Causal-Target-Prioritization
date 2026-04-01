import Link from "next/link";

import { HowRankingWorks } from "@/components/how-ranking-works";
import { MetricStrip } from "@/components/metric-strip";
import { PageShell } from "@/components/page-shell";
import { TargetRankingTable } from "@/components/target-ranking-table";
import { fetchDiseaseSummary, fetchRankedTargets } from "@/lib/api";
import { normalizeIdentifier } from "@/lib/identifiers";
import { compareHref, diseaseHref } from "@/lib/urls";

export const dynamic = "force-dynamic";

export default async function DiseaseWorkspacePage({
  params
}: {
  params: Promise<{ id: string }>;
}) {
  const { id: rawId } = await params;
  const id = normalizeIdentifier(rawId) ?? rawId;
  const [rankedTargets, diseaseMeta] = await Promise.all([
    fetchRankedTargets(id),
    fetchDiseaseSummary(id)
  ]);
  const diseaseLabel = diseaseMeta?.label ?? id;

  return (
    <PageShell
      title={diseaseLabel}
      eyebrow="Balanced profile with transparent evidence components and safety drag."
      breadcrumbs={[
        { label: "Home", href: "/" },
        { label: "Disease", href: diseaseHref(id) },
        { label: diseaseLabel }
      ]}
      contextStrip={`${diseaseLabel} · ${id}`}
      copyActions={[{ label: "Copy disease ID", value: id }]}
    >
      <MetricStrip
        items={[
          { label: "Disease", value: diseaseLabel },
          { label: "Disease ID", value: id },
          { label: "Top target", value: rankedTargets[0]?.targetSymbol ?? "N/A" },
          { label: "Visible shortlist", value: `${rankedTargets.length}` }
        ]}
      />

      <div className="mb-6">
        <HowRankingWorks />
      </div>

      <TargetRankingTable diseaseId={id} items={rankedTargets} />

      <section className="mt-8 border border-border bg-bg-muted/50 p-6 md:p-8">
        <h2 className="font-display text-lg font-bold text-fg">Suggested comparison</h2>
        <p className="mt-2 text-sm text-fg-muted">Open the first two targets in side-by-side mode.</p>
        <Link
          className="ds-link-cta ds-link-cta--primary mt-5 inline-flex normal-case tracking-normal"
          href={compareHref(
            id,
            rankedTargets.slice(0, 2).map((item) => item.targetId)
          )}
        >
          Compare top 2
        </Link>
      </section>
    </PageShell>
  );
}
