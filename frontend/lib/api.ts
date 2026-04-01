import {
  DiseaseSummary,
  SourceStatus,
  TargetDetail,
  TargetScorecard
} from "@/lib/types";


const DEFAULT_API_BASE_URLS = process.env.CTPC_API_BASE_URL
  ? [process.env.CTPC_API_BASE_URL]
  : [
      "http://127.0.0.1:8010",
      "http://localhost:8010",
      "http://127.0.0.1:8000",
      "http://localhost:8000"
    ];

let resolvedApiBaseUrl: string | null = null;

export function resetApiBaseUrlCache() {
  resolvedApiBaseUrl = null;
}

async function resolveApiBaseUrl(): Promise<string> {
  if (resolvedApiBaseUrl) {
    return resolvedApiBaseUrl;
  }

  for (const candidate of DEFAULT_API_BASE_URLS) {
    try {
      const response = await fetch(`${candidate}/healthz`, {
        cache: "no-store"
      });

      if (!response.ok) {
        continue;
      }

      const payload = (await response.json()) as { service?: string };
      if (payload.service === "ctpc-backend") {
        resolvedApiBaseUrl = candidate;
        return candidate;
      }
    } catch {
      continue;
    }
  }

  resolvedApiBaseUrl = DEFAULT_API_BASE_URLS[0];
  return resolvedApiBaseUrl;
}

async function readJson<T>(path: string): Promise<T> {
  const apiBaseUrl = await resolveApiBaseUrl();
  const requestUrl = `${apiBaseUrl}${path}`;
  const response = await fetch(requestUrl, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`API request failed for ${requestUrl}: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function fetchDiseases(query = "ulcerative"): Promise<DiseaseSummary[]> {
  const payload = await readJson<{ items: DiseaseSummary[] }>(
    `/api/v1/diseases?query=${encodeURIComponent(query)}`
  );

  return payload.items;
}

export async function fetchDiseaseSummary(diseaseId: string): Promise<DiseaseSummary | null> {
  try {
    return await readJson<DiseaseSummary>(`/api/v1/diseases/${encodeURIComponent(diseaseId)}`);
  } catch {
    return null;
  }
}

export async function fetchRankedTargets(
  diseaseId: string,
  profile = "balanced"
): Promise<TargetScorecard[]> {
  const payload = await readJson<{ items: TargetScorecard[] }>(
    `/api/v1/diseases/${encodeURIComponent(diseaseId)}/targets?profile=${encodeURIComponent(profile)}`
  );

  return payload.items;
}

export async function fetchTargetDetail(
  targetId: string,
  diseaseId: string
): Promise<TargetDetail> {
  return readJson<TargetDetail>(
    `/api/v1/targets/${encodeURIComponent(targetId)}?disease_id=${encodeURIComponent(diseaseId)}`
  );
}

export async function fetchCompareTargets(
  diseaseId: string,
  targetIds: string[]
): Promise<TargetScorecard[]> {
  const params = new URLSearchParams({ disease_id: diseaseId });
  targetIds.forEach((targetId) => params.append("target_ids", targetId));
  const payload = await readJson<{ items: TargetScorecard[] }>(`/api/v1/compare?${params.toString()}`);
  return payload.items;
}

export async function fetchSourceStatus(): Promise<SourceStatus[]> {
  const payload = await readJson<{ items: SourceStatus[] }>("/api/v1/admin/sources");
  return payload.items;
}
