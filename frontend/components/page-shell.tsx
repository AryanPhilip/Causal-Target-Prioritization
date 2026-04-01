import Link from "next/link";
import { ReactNode } from "react";

import { Breadcrumbs, type Crumb } from "@/components/breadcrumbs";
import { CopyButton } from "@/components/copy-button";
import { SiteFooter } from "@/components/site-footer";
import { ThemeToggle } from "@/components/theme-selector";
import { compareHref, diseaseHref } from "@/lib/urls";

export const DEFAULT_DISEASE_ID = "MONDO:0005101";

type PageShellProps = {
  title: string;
  eyebrow?: string;
  children: ReactNode;
  breadcrumbs?: Crumb[];
  /** Shown under breadcrumbs: e.g. disease id, optional meta */
  contextStrip?: string;
  /** Optional clipboard actions next to the context line */
  copyActions?: Array<{ label: string; value: string }>;
};

const navLink =
  "border border-transparent px-2 py-1.5 text-[0.75rem] font-semibold uppercase tracking-[0.14em] text-fg-muted transition-[color,border-color,background-color] duration-[420ms] ease-[cubic-bezier(0.22,1,0.36,1)] hover:border-border hover:bg-bg-elevated hover:text-fg focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring";

export function PageShell({
  title,
  eyebrow,
  children,
  breadcrumbs,
  contextStrip,
  copyActions
}: PageShellProps) {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-20 border-b border-border bg-bg/92 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-5 py-4 md:px-8">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div className="flex min-w-0 flex-wrap items-baseline gap-3">
              <Link
                href="/"
                className="border-l-4 border-accent pl-3 font-display text-base font-bold tracking-tight text-fg md:text-lg"
              >
                CTPC
              </Link>
              <span className="hidden text-border-strong sm:inline" aria-hidden>
                |
              </span>
              <span className="text-xs font-medium uppercase tracking-[0.14em] text-fg-muted">
                Causal target prioritization
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              <nav aria-label="Primary" className="flex flex-wrap gap-1">
                <Link href="/" className={navLink}>
                  Home
                </Link>
                <Link href={diseaseHref(DEFAULT_DISEASE_ID)} className={navLink}>
                  Workspace
                </Link>
                <Link href={compareHref(DEFAULT_DISEASE_ID)} className={navLink}>
                  Compare
                </Link>
                <Link href="/admin/status" className={navLink}>
                  Admin
                </Link>
              </nav>
              <ThemeToggle />
            </div>
          </div>
        </div>
      </header>

      <main id="main-content" className="mx-auto w-full max-w-6xl flex-1 px-5 py-8 md:px-8 md:py-10">
        {breadcrumbs && breadcrumbs.length > 0 ? <Breadcrumbs items={breadcrumbs} /> : null}
        {contextStrip ? (
          <div className="mb-4 flex flex-wrap items-center gap-2">
            <p className="max-w-3xl text-sm leading-relaxed text-fg-muted">{contextStrip}</p>
            {copyActions?.map((action) => (
              <CopyButton key={action.label} label={action.label} text={action.value} />
            ))}
          </div>
        ) : null}
        <div className="mb-8 border-b border-border pb-8">
          <div className="flex items-center gap-3">
            <span className="h-0.5 w-10 shrink-0 bg-accent" aria-hidden />
            <p className="text-[0.65rem] font-semibold uppercase tracking-[0.2em] text-accent">CTPC</p>
          </div>
          <h1 className="mt-4 font-display text-3xl font-bold tracking-tight text-fg md:text-4xl">
            {title}
          </h1>
          {eyebrow ? (
            <p className="mt-3 max-w-3xl text-base leading-relaxed text-fg-muted">{eyebrow}</p>
          ) : null}
        </div>
        {children}
        <SiteFooter />
      </main>
    </div>
  );
}
