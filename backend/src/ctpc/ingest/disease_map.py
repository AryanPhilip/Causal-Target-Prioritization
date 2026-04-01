"""Map frontend disease IDs (e.g. MONDO) to OpenTargets Platform disease IDs (often EFO)."""

# OpenTargets GraphQL uses Platform disease ids; MONDO ids often need explicit mapping.
MONDO_TO_OPENTARGETS: dict[str, str] = {
    "MONDO:0005101": "EFO_0000729",  # ulcerative colitis
}


def resolve_for_opentargets(disease_id: str) -> str:
    if disease_id in MONDO_TO_OPENTARGETS:
        return MONDO_TO_OPENTARGETS[disease_id]
    if disease_id.startswith("MONDO:") or disease_id.startswith("EFO:") or disease_id.startswith("Orphanet:"):
        return disease_id.replace(":", "_")
    return disease_id
