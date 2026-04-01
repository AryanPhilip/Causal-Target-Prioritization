"""ClinicalTrials.gov API v2."""

from __future__ import annotations

import logging
import math

import httpx

from ctpc.config import get_settings

log = logging.getLogger(__name__)


def search_trials_for_target(
    symbol: str,
    disease_terms: str = "ulcerative colitis",
    page_size: int = 20,
    client: httpx.Client | None = None,
) -> list[dict]:
    settings = get_settings()
    own = client is None
    c = client or httpx.Client(timeout=settings.http_timeout_seconds)
    try:
        q = f"{symbol} AND {disease_terms}"
        r = c.get(
            settings.clinicaltrials_api_url,
            params={
                "query.term": q,
                "pageSize": page_size,
                "format": "json",
            },
        )
        if r.status_code != 200:
            return []
        data = r.json()
        studies = data.get("studies") or []
        out: list[dict] = []
        for s in studies:
            proto = (s.get("protocolSection") or {}) if isinstance(s, dict) else {}
            ident = proto.get("identificationModule") or {}
            status_mod = proto.get("statusModule") or {}
            design = proto.get("designModule") or {}
            nct = ident.get("nctId") or ""
            title = ident.get("briefTitle") or ident.get("officialTitle") or ""
            phases = design.get("phases") or []
            phase = ", ".join(phases) if phases else "N/A"
            st = status_mod.get("overallStatus") or "UNKNOWN"
            if nct:
                out.append(
                    {
                        "nctId": nct,
                        "title": title[:500],
                        "phase": phase[:64],
                        "status": st[:64],
                    }
                )
        return out
    except Exception as e:
        log.debug("clinicaltrials: %s", e)
        return []
    finally:
        if own:
            c.close()


def clinical_support_score(n_trials: int) -> float:
    if n_trials <= 0:
        return 0.0
    return min(100.0, 22.0 * math.log2(1 + n_trials))
