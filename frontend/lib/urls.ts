/**
 * Path segments that include reserved characters (e.g. MONDO:0005101) must be encoded
 * or dynamic routes can 404 in the App Router.
 */
export function diseaseHref(id: string): string {
  return `/disease/${encodeURIComponent(id)}`;
}

export function targetHref(targetId: string, diseaseId: string): string {
  const q = new URLSearchParams({ diseaseId });
  return `/target/${encodeURIComponent(targetId)}?${q.toString()}`;
}

export function compareHref(diseaseId: string, targetIds?: string[]): string {
  const q = new URLSearchParams();
  q.set("diseaseId", diseaseId);
  if (targetIds?.length) {
    q.set("targetIds", targetIds.join(","));
  }
  return `/compare?${q.toString()}`;
}
