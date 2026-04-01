"""Deterministic scoring from raw component signals (0–100 scales)."""

from __future__ import annotations

import math


def overall_score(
    association: float,
    clinical: float,
    chemical: float,
    tractability: float,
    confidence_modifier: float,
    safety_penalty: float,
) -> float:
    """Weighted sum minus safety drag; result on ~0–100 scale."""
    base = (
        0.26 * association
        + 0.24 * clinical
        + 0.20 * chemical
        + 0.18 * tractability
        + 0.12 * confidence_modifier
    )
    return max(0.0, min(100.0, base - 0.35 * safety_penalty))


def confidence_label_from_modifier(mod: float) -> str:
    if mod >= 7.5:
        return "High"
    if mod >= 4.0:
        return "Medium"
    return "Low"


def percentiles_from_scores(scores: list[float]) -> list[float]:
    """Percentile rank 0–100 (higher score = higher percentile)."""
    if not scores:
        return []
    sorted_vals = sorted(scores)
    n = len(sorted_vals)
    out: list[float] = []
    for s in scores:
        # fraction of values strictly below s
        below = sum(1 for x in sorted_vals if x < s)
        pct = 100.0 * below / max(1, n - 1) if n > 1 else 50.0
        out.append(round(pct, 1))
    return out


def modifier_from_association(assoc_01: float) -> float:
    """Map 0–1 association to 0–10 confidence modifier."""
    return round(min(10.0, 3.0 + 7.0 * assoc_01), 2)


def safety_penalty_heuristic(trial_titles: str, n_trials: int) -> float:
    """Heuristic AE burden from trial text keywords + volume."""
    t = trial_titles.lower()
    risk = 0.0
    if any(k in t for k in ("serious adverse", "infection", "malignancy", "death")):
        risk += 25.0
    if "warning" in t or "black box" in t:
        risk += 15.0
    risk += min(35.0, 4.0 * math.log2(1 + max(0, n_trials - 1)))
    return min(100.0, risk)
