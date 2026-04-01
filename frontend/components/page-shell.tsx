import Link from "next/link";
import { ReactNode } from "react";

import { Breadcrumbs, type Crumb } from "@/components/breadcrumbs";
import { CopyButton } from "@/components/copy-button";
import { SiteFooter } from "@/components/site-footer";
import { TextScaleSelector } from "@/components/text-scale-selector";
import { ThemeSelector } from "@/components/theme-selector";
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

export function PageShell({
  title,
  eyebrow,
  children,
  breadcrumbs,
  contextStrip,
  copyActions
}: PageShellProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="sticky top-0 z-20 border-b border-border bg-bg/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-5 py-4 md:px-8">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div className="flex min-w-0 flex-wrap items-baseline gap-3">
              <Link
                href="/"
                className="font-display text-base font-semibold tracking-tight text-fg md:text-lg"
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
            <div className="flex flex-col gap-4 sm:flex-row sm:flex-wrap sm:items-start sm:gap-6">
              <nav aria-label="Primary" className="flex flex-wrap gap-2">
                <Link
                  href="/"
                  className="rounded-full border border-transparent px-3 py-1.5 text-sm font-medium text-fg-muted transition hover:border-border hover:bg-bg-elevated hover:text-fg"
                >
                  Home
                </Link>
                <Link
                  href={diseaseHref(DEFAULT_DISEASE_ID)}
                  className="rounded-full border border-transparent px-3 py-1.5 text-sm font-medium text-fg-muted transition hover:border-border hover:bg-bg-elevated hover:text-fg"
                >
                  Workspace
                </Link>
                <Link
                  href={compareHref(DEFAULT_DISEASE_ID)}
                  className="rounded-full border border-transparent px-3 py-1.5 text-sm font-medium text-fg-muted transition hover:border-border hover:bg-bg-elevated hover:text-fg"
                >
                  Compare
                </Link>
                <Link
                  href="/admin/status"
                  className="rounded-full border border-transparent px-3 py-1.5 text-sm font-medium text-fg-muted transition hover:border-border hover:bg-bg-elevated hover:text-fg"
                >
                  Admin
                </Link>
              </nav>
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:gap-5">
                <ThemeSelector />
                <TextScaleSelector />
              </div>
            </div>
          </div>
        </div>
      </header>

      <main id="main-content" className="mx-auto w-full max-w-6xl flex-1 px-5 py-8 md:px-8 md:py-10">
        {breadcrumbs && breadcrumbs.length > 0 ? <Breadcrumbs items={breadcrumbs} /> : null}
        {contextStrip ? (
          <div className="mb-4 flex flex-wrap items-center gap-2">
            <p className="font-mono text-xs leading-relaxed text-fg-muted tabular-nums">{contextStrip}</p>
            {copyActions?.map((action) => (
              <CopyButton key={action.label} label={action.label} text={action.value} />
            ))}
          </div>
        ) : null}
        <div className="mb-8 border-b border-border pb-8">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-accent">CTPC</p>
          <h1 className="mt-2 font-display text-3xl font-semibold tracking-tight text-fg md:text-4xl">
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
