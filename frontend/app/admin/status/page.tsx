import { PageShell } from "@/components/page-shell";
import { SourceStatusPanel } from "@/components/source-status-panel";
import { fetchSourceStatus } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function AdminStatusPage() {
  const items = await fetchSourceStatus();

  return (
    <PageShell
      title="Admin · source status"
      eyebrow="Minimal governance surface for source freshness, row counts, and validation state."
      breadcrumbs={[{ label: "Home", href: "/" }, { label: "Admin" }]}
    >
      <SourceStatusPanel items={items} />
    </PageShell>
  );
}
