const PILLARS = [
  {
    title: "Trials & clinical",
    detail: "Structured trial metadata and phase signals grounded in public registries."
  },
  {
    title: "Compounds & modality",
    detail: "Chemical matter and modality context to separate tractable from speculative."
  },
  {
    title: "Safety & burden",
    detail: "Adverse-event and safety penalties that temper enthusiasm when risk rises."
  }
] as const;

export function TrustStrip() {
  return (
    <section
      aria-labelledby="trust-heading"
      className="rounded-[var(--radius-lg)] border border-border bg-bg-elevated p-6 shadow-[var(--shadow-elevated)] md:p-8"
    >
      <h2 id="trust-heading" className="font-display text-lg font-semibold tracking-tight text-fg md:text-xl">
        Evidence classes in this vertical
      </h2>
      <p className="mt-2 max-w-3xl text-sm leading-relaxed text-fg-muted">
        CTPC ranks targets using an explainable causal evidence profile—not a black-box score. Each
        pillar below maps to measurable inputs the engine can cite and you can inspect.
      </p>
      <ul className="mt-6 grid gap-4 md:grid-cols-3">
        {PILLARS.map((p) => (
          <li
            key={p.title}
            className="rounded-2xl border border-border bg-bg-muted/60 p-4 transition hover:border-border-strong"
          >
            <h3 className="text-sm font-semibold text-fg">{p.title}</h3>
            <p className="mt-2 text-xs leading-relaxed text-fg-muted">{p.detail}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
