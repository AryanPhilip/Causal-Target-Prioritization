"""OpenTargets Platform API (GraphQL v4)."""

from __future__ import annotations

import logging
from dataclasses import dataclass

import httpx

from ctpc.config import get_settings
from ctpc.ingest.disease_map import resolve_for_opentargets

log = logging.getLogger(__name__)

GRAPHQL_QUERY = """
query DiseaseTargets($efoId: String!, $size: Int!) {
  disease(efoId: $efoId) {
    id
    name
    associatedTargets(page: { size: $size, index: 0 }) {
      count
      rows {
        score
        target {
          id
          approvedSymbol
          approvedName
        }
      }
    }
  }
}
"""


@dataclass
class AssociatedTarget:
    ensembl_id: str
    symbol: str
    name: str
    association_score: float


def fetch_disease_associated_targets(
    mondo_id: str,
    *,
    limit: int = 50,
    client: httpx.Client | None = None,
) -> tuple[str, str, list[AssociatedTarget]]:
    """Returns (disease_ot_id, disease_name, targets)."""
    settings = get_settings()
    efo_id = resolve_for_opentargets(mondo_id)
    own_client = client is None
    c = client or httpx.Client(timeout=settings.http_timeout_seconds)

    try:
        gql_url = settings.opentargets_api_url.rstrip("/") + "/graphql"
        r = c.post(
            gql_url,
            json={
                "query": GRAPHQL_QUERY,
                "variables": {"efoId": efo_id, "size": limit},
            },
        )
        r.raise_for_status()
        payload = r.json()
        if "errors" in payload and payload["errors"]:
            log.warning("GraphQL errors: %s", payload["errors"])
        data = payload.get("data") or {}
        disease = data.get("disease")
        if not disease:
            return efo_id, mondo_id, []
        name = disease.get("name") or mondo_id
        at = disease.get("associatedTargets") or {}
        rows = at.get("rows") or []
        out: list[AssociatedTarget] = []
        for row in rows:
            t = row.get("target") or {}
            tid = t.get("id") or ""
            if not tid.startswith("ENSG"):
                continue
            score = float(row.get("score") or 0)
            out.append(
                AssociatedTarget(
                    ensembl_id=tid,
                    symbol=t.get("approvedSymbol") or tid,
                    name=t.get("approvedName") or tid,
                    association_score=min(1.0, max(0.0, score)),
                )
            )
        return disease.get("id") or efo_id, name, out
    finally:
        if own_client:
            c.close()


UNIPROT_QUERY = """
query Tprot($ensemblId: String!) {
  target(ensemblId: $ensemblId) {
    proteinIds { id source }
  }
}
"""


def fetch_uniprot_swissprot(
    ensembl_id: str,
    *,
    client: httpx.Client | None = None,
) -> str | None:
    settings = get_settings()
    own_client = client is None
    c = client or httpx.Client(timeout=settings.http_timeout_seconds)
    try:
        gql_url = settings.opentargets_api_url.rstrip("/") + "/graphql"
        r = c.post(
            gql_url,
            json={"query": UNIPROT_QUERY, "variables": {"ensemblId": ensembl_id}},
        )
        r.raise_for_status()
        data = (r.json().get("data") or {}).get("target") or {}
        for pid in data.get("proteinIds") or []:
            if pid.get("source") == "uniprot_swissprot":
                return pid.get("id")
        for pid in data.get("proteinIds") or []:
            if pid.get("id"):
                return pid.get("id")
        return None
    except Exception as e:
        log.debug("uniprot lookup %s: %s", ensembl_id, e)
        return None
    finally:
        if own_client:
            c.close()


def tractability_score(association_01: float) -> float:
    """0–100 tractability proxy when ChEMBL/OT tractability is expensive."""
    return min(100.0, max(15.0, 20.0 + 80.0 * association_01))
