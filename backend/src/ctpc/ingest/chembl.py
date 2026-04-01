"""ChEMBL REST API — compounds / mechanisms for a target."""

from __future__ import annotations

import logging
import math

import httpx

from ctpc.config import get_settings

log = logging.getLogger(__name__)


def resolve_chembl_target_id(
    ensembl_id: str,
    uniprot_accession: str | None,
    client: httpx.Client | None = None,
) -> str | None:
    """Resolve ChEMBL target id via UniProt (ChEMBL indexes protein accessions reliably)."""
    settings = get_settings()
    own = client is None
    c = client or httpx.Client(timeout=settings.http_timeout_seconds)
    try:
        if uniprot_accession:
            r = c.get(
                f"{settings.chembl_api_url}/target.json",
                params={"target_components__accession": uniprot_accession, "limit": 1},
            )
            if r.status_code == 200:
                data = r.json()
                rows = data.get("targets") or []
                if rows:
                    return rows[0].get("target_chembl_id")
        r = c.get(
            f"{settings.chembl_api_url}/target.json",
            params={"target_components__accession": ensembl_id, "limit": 1},
        )
        if r.status_code == 200:
            data = r.json()
            rows = data.get("targets") or []
            if rows:
                return rows[0].get("target_chembl_id")
        return None
    finally:
        if own:
            c.close()


def count_mechanism_drugs(chembl_target_id: str, client: httpx.Client | None = None) -> int:
    settings = get_settings()
    own = client is None
    c = client or httpx.Client(timeout=settings.http_timeout_seconds)
    try:
        r = c.get(
            f"{settings.chembl_api_url}/mechanism.json",
            params={"target_chembl_id": chembl_target_id, "limit": 1},
        )
        if r.status_code != 200:
            return 0
        data = r.json()
        meta = data.get("page_meta") or {}
        total = meta.get("total_count")
        if total is not None:
            return int(total)
        mechs = data.get("mechanisms") or []
        return len(mechs)
    finally:
        if own:
            c.close()


def fetch_top_compounds(
    chembl_target_id: str,
    limit: int = 5,
    client: httpx.Client | None = None,
) -> list[dict]:
    """Return [{chembl_id, name, modality}] from mechanisms + molecule."""
    settings = get_settings()
    own = client is None
    c = client or httpx.Client(timeout=settings.http_timeout_seconds)
    out: list[dict] = []
    try:
        r = c.get(
            f"{settings.chembl_api_url}/mechanism.json",
            params={"target_chembl_id": chembl_target_id, "limit": limit},
        )
        if r.status_code != 200:
            return out
        data = r.json()
        mechs = data.get("mechanisms") or []
        seen: set[str] = set()
        for m in mechs:
            mid = m.get("molecule_chembl_id")
            if not mid or mid in seen:
                continue
            seen.add(mid)
            modality = "small molecule"
            if m.get("action_type"):
                modality = str(m.get("action_type"))
            mr = c.get(f"{settings.chembl_api_url}/molecule/{mid}.json")
            name = mid
            if mr.status_code == 200:
                mj = mr.json()
                name = mj.get("pref_name") or mj.get("molecule_chembl_id") or mid
            out.append({"chemblId": mid, "name": name, "modality": modality})
            if len(out) >= limit:
                break
        return out
    except Exception as e:
        log.debug("chembl compounds: %s", e)
        return out
    finally:
        if own:
            c.close()


def chemical_support_score(drug_count: int) -> float:
    """Map mechanism drug count to 0..100."""
    if drug_count <= 0:
        return 0.0
    return min(100.0, 18.0 * math.sqrt(drug_count))
