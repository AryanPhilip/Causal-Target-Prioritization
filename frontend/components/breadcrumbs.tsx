import Link from "next/link";

export type Crumb = { label: string; href?: string };

type BreadcrumbsProps = {
  items: Crumb[];
};

export function Breadcrumbs({ items }: BreadcrumbsProps) {
  if (items.length === 0) {
    return null;
  }

  return (
    <nav aria-label="Breadcrumb" className="mb-6 text-sm text-fg-muted">
      <ol className="flex flex-wrap items-center gap-2">
        {items.map((item, i) => {
          const isLast = i === items.length - 1;
          return (
            <li key={`${item.label}-${i}`} className="flex items-center gap-2">
              {i > 0 ? (
                <span className="text-border-strong" aria-hidden>
                  /
                </span>
              ) : null}
              {isLast || !item.href ? (
                <span className={isLast ? "font-medium text-fg" : undefined}>{item.label}</span>
              ) : (
                <Link
                  href={item.href}
                  className="rounded-sm text-accent underline-offset-4 hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                >
                  {item.label}
                </Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
