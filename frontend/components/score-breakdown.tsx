import { TargetScorecard } from "@/lib/types";

type ScoreBreakdownProps = {
  components: TargetScorecard["components"];
};

export function ScoreBreakdown({ components }: ScoreBreakdownProps) {
  const rows: Array<{
    label: string;
    display: string;
    pct: number;
    variant: "accent" | "risk";
  }> = [
    {
      label: "Association",
      display: String(components.associationEvidence),
      pct: clampPct(components.associationEvidence, 100),
      variant: "accent"
    },
    {
      label: "Clinical",
      display: String(components.clinicalSupport),
      pct: clampPct(components.clinicalSupport, 100),
      variant: "accent"
    },
    {
      label: "Chemical",
      display: String(components.chemicalSupport),
      pct: clampPct(components.chemicalSupport, 100),
      variant: "accent"
    },
    {
      label: "Tractability",
      display: String(components.tractability),
      pct: clampPct(components.tractability, 100),
      variant: "accent"
    },
    {
      label: "Confidence",
      display: String(components.confidenceModifier),
      pct: clampPct(components.confidenceModifier, 10),
      variant: "accent"
    },
    {
      label: "Safety burden",
      display: `−${components.safetyPenalty}`,
      pct: clampPct(components.safetyPenalty, 100),
      variant: "risk"
    }
  ];

  return (
    <div className="space-y-3" role="group" aria-label="Score components">
      {rows.map((row) => (
        <div key={row.label}>
          <div className="mb-1 flex justify-between text-xs">
            <span className="font-medium text-fg-muted">{row.label}</span>
            <span className="tabular-nums text-fg">{row.display}</span>
          </div>
          <div
            className="h-1.5 overflow-hidden rounded-[var(--radius-lg)] border border-border bg-bg-muted"
            role="presentation"
            aria-hidden
          >
            <div
              className={
                row.variant === "risk"
                  ? "h-full bg-gradient-to-r from-danger/90 to-warn/80"
                  : "h-full bg-gradient-to-r from-accent/90 to-accent/45"
              }
              style={{ width: `${row.pct}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}

function clampPct(value: number, max: number): number {
  if (!Number.isFinite(value) || max <= 0) {
    return 0;
  }
  const pct = (value / max) * 100;
  return Math.max(0, Math.min(100, pct));
}
