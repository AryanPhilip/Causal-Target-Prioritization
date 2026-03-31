import { ReactNode } from "react";

type SectionProps = {
  id?: string;
  title: string;
  description?: string;
  children: ReactNode;
  className?: string;
};

export function Section({ id, title, description, children, className = "" }: SectionProps) {
  return (
    <section
      id={id}
      className={`ds-panel border-border-strong p-6 md:p-8 ${className}`}
    >
      <header className="mb-5">
        <h2 className="font-display text-lg font-bold tracking-tight text-fg md:text-xl">{title}</h2>
        {description ? <p className="mt-2 max-w-3xl text-sm text-fg-muted">{description}</p> : null}
      </header>
      {children}
    </section>
  );
}
