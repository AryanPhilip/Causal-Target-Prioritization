"""Normalize disease / target identifiers across sources."""


def mondo_to_ot_path(mondo: str) -> str:
    """OpenTargets Platform REST paths use MONDO_0005101 style."""
    s = mondo.strip()
    if ":" in s:
        prefix, rest = s.split(":", 1)
        return f"{prefix}_{rest}"
    return s.replace(":", "_")


def ot_path_to_mondo(ot_id: str) -> str:
    if "_" in ot_id and not ot_id.startswith("ENSG"):
        parts = ot_id.split("_", 1)
        if len(parts) == 2 and parts[0] in ("MONDO", "EFO", "Orphanet"):
            return f"{parts[0]}:{parts[1]}"
    return ot_id
