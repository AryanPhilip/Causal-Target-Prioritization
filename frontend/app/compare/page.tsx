import Link from "next/link";

import { PageShell } from "@/components/page-shell";
import { fetchCompareTargets } from "@/lib/api";
import { normalizeIdentifier } from "@/lib/identifiers";
import { diseaseHref } from "@/lib/urls";

export const dynamic = "force-dynamic";

export default async function ComparePage({
  searchParams
}: {
  searchParams: Promise<{ diseaseId?: string; targetIds?: string }>;
}) {
  const { diseaseId: rawDiseaseId = "MONDO:0005101", targetIds = "" } = await searchParams;
  const diseaseId = normalizeIdentifier(rawDiseaseId) ?? rawDiseaseId;
  const ids = targetIds.split(",").filter(Boolean);
  const items = ids.length > 0 ? await fetchCompareTargets(diseaseId, ids) : [];

  return (
    <PageShell
      title="Compare targets"
      eyebrow="Side-by-side readout of evidence weight, safety drag, and headline rationale."
      breadcrumbs={[
        { label: "Home", href: "/" },
        { label: "Compare" }
      ]}
      contextStrip={`Disease ${diseaseId}`}
      copyActions={[{ label: "Copy disease ID", value: diseaseId }]}
    >
      {items.length === 0 ? (
        <div className="border border-dashed border-border bg-bg-muted/40 p-8 text-center">
          <p className="text-fg-muted">
            Pick at least one target from the{" "}
            <Link className="font-semibold text-accent underline-offset-4 hover:underline" href={diseaseHref("MONDO:0005101")}>
              disease workspace
            </Link>
            .
          </p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {items.map((item) => (
            <section
              className="detail-card border border-border-strong bg-bg-elevated p-6 shadow-[var(--shadow-elevated)]"
              key={item.targetId}
            >
              <h2 className="font-mono text-lg font-semibold text-fg">{item.targetSymbol}</h2>
              <p className="mt-1 text-sm text-fg-muted">{item.targetName}</p>
              <p className="mt-4 font-display text-3xl font-bold tabular-nums text-fg">
                {item.overallScore}
              </p>
              <p className="mt-4 text-sm leading-relaxed text-fg-muted">{item.explanation.summary}</p>
            </section>
          ))}
        </div>
      )}
    </PageShell>
  );
}
