"use client";

import Link from "next/link";
import { useEffect, useId, useState } from "react";

import { fetchDiseases } from "@/lib/api";
import type { DiseaseSummary } from "@/lib/types";
import { diseaseHref } from "@/lib/urls";

type DiseaseSearchProps = {
  /** Server-rendered results for first paint */
  initialItems: DiseaseSummary[];
  initialQuery?: string;
};

export function DiseaseSearch({ initialItems, initialQuery = "ulcerative" }: DiseaseSearchProps) {
  const listId = useId();
  const [query, setQuery] = useState(initialQuery);
  const [items, setItems] = useState<DiseaseSummary[]>(initialItems);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const q = query.trim();
    const handle = window.setTimeout(async () => {
      setLoading(true);
      try {
        const next = await fetchDiseases(q.length > 0 ? q : "");
        if (!cancelled) {
          setItems(next);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }, 280);

    return () => {
      cancelled = true;
      window.clearTimeout(handle);
    };
  }, [query]);

  return (
    <div className="mt-6 flex flex-col gap-3">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <label className="sr-only" htmlFor={`${listId}-input`}>
          Search diseases in the database
        </label>
        <input
          id={`${listId}-input`}
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by disease name…"
          autoComplete="off"
          className="min-w-0 flex-1 rounded-[var(--radius-lg)] border border-border-strong bg-bg-muted px-4 py-3 text-sm text-fg shadow-[var(--shadow-tight)] outline-none ring-ring/0 transition-[border-color,box-shadow] duration-[420ms] ease-[cubic-bezier(0.22,1,0.36,1)] focus:border-accent focus:ring-2 focus:ring-ring"
          aria-controls={listId}
          aria-busy={loading}
        />
      </div>
      <div
        id={listId}
        role="listbox"
        aria-label="Disease search results"
        className="max-h-56 overflow-auto rounded-[var(--radius-lg)] border border-border-strong bg-bg-elevated shadow-[var(--shadow-tight)]"
      >
        {items.length === 0 ? (
          <p className="px-4 py-6 text-center text-sm text-fg-muted">
            {loading ? "Searching…" : "No diseases match that query."}
          </p>
        ) : (
          <ul className="divide-y divide-border">
            {items.map((d) => (
              <li key={d.id} role="none">
                <Link
                  role="option"
                  href={diseaseHref(d.id)}
                  className="block px-4 py-3 transition-[background-color] duration-[420ms] ease-[cubic-bezier(0.22,1,0.36,1)] hover:bg-bg-muted"
                >
                  <span className="font-medium text-fg">{d.label}</span>
                  <span className="mt-0.5 block font-mono text-xs tabular-nums text-fg-muted">{d.id}</span>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
      <p className="text-xs text-fg-muted">Results come from the CTPC API (Postgres disease catalog). Choose a row to open that disease workspace.</p>
    </div>
  );
}
