from __future__ import annotations

from dataclasses import dataclass

from ctpc.core.types import EvidenceItem, Explanation, RankingProfile, ScoreComponents, TargetScorecard
from ctpc.data.fixtures import RANKING_FIXTURES, UC_DISEASE


@dataclass(frozen=True)
class RankingInput:
    target_id: str
    target_symbol: str
    target_name: str
    association_evidence: float
    clinical_support: float
    chemical_support: float
    tractability: float
    confidence_modifier: float
    serious_event_count: int
    warning_flag: bool
    freshness_days: int = 2
    confidence_label: str = "high"


@dataclass(frozen=True)
class ProfileWeights:
    association: float
    clinical: float
    chemical: float
    tractability: float
    confidence_cap: float
    safety_multiplier: float


PROFILE_WEIGHTS = {
    RankingProfile.BALANCED: ProfileWeights(0.40, 0.25, 0.20, 0.10, 5.0, 1.0),
    RankingProfile.CONSERVATIVE: ProfileWeights(0.35, 0.30, 0.15, 0.10, 5.0, 1.5),
    RankingProfile.INNOVATION: ProfileWeights(0.50, 0.15, 0.15, 0.10, 10.0, 0.75),
}


def rank_targets_for_disease(
    disease_id: str,
    profile: RankingProfile = RankingProfile.BALANCED,
) -> list[TargetScorecard]:
    if disease_id != UC_DISEASE.id:
        return []

    scorecards = [
        build_scorecard(
            RankingInput(
                target_id=target["target_id"],
                target_symbol=target["target_symbol"],
                target_name=target["target_name"],
                association_evidence=float(target["association_evidence"]),
                clinical_support=float(target["clinical_support"]),
                chemical_support=float(target["chemical_support"]),
                tractability=float(target["tractability"]),
                confidence_modifier=float(target["confidence_modifier"]),
                serious_event_count=int(target["serious_event_count"]),
                warning_flag=bool(target["warning_flag"]),
            ),
            profile,
            disease_id=UC_DISEASE.id,
            disease_name=UC_DISEASE.label,
            supporting_evidence=target["supporting_evidence"],
            risk_evidence=target["risk_evidence"],
        )
        for target in RANKING_FIXTURES
    ]
    return sorted(scorecards, key=lambda item: item.overall_score, reverse=True)


def build_scorecard(
    ranking_input: RankingInput,
    profile: RankingProfile,
    disease_id: str,
    disease_name: str,
    supporting_evidence: list[dict[str, object]],
    risk_evidence: list[dict[str, object]],
) -> TargetScorecard:
    weights = PROFILE_WEIGHTS[profile]
    safety_penalty = _calculate_safety_penalty(
        ranking_input.serious_event_count,
        ranking_input.warning_flag,
        weights.safety_multiplier,
    )
    confidence_modifier = min(ranking_input.confidence_modifier, weights.confidence_cap)
    overall_score = _clamp(
        ranking_input.association_evidence * weights.association
        + ranking_input.clinical_support * weights.clinical
        + ranking_input.chemical_support * weights.chemical
        + ranking_input.tractability * weights.tractability
        + confidence_modifier
        - safety_penalty
    )
    rounded_score = round(overall_score, 1)
    return TargetScorecard(
        targetId=ranking_input.target_id,
        targetSymbol=ranking_input.target_symbol,
        targetName=ranking_input.target_name,
        diseaseId=disease_id,
        diseaseName=disease_name,
        overallScore=rounded_score,
        percentile=_percentile_for_score(rounded_score),
        profile=profile,
        components=ScoreComponents(
            associationEvidence=ranking_input.association_evidence,
            clinicalSupport=ranking_input.clinical_support,
            chemicalSupport=ranking_input.chemical_support,
            tractability=ranking_input.tractability,
            confidenceModifier=round(confidence_modifier, 1),
            safetyPenalty=round(safety_penalty, 1),
        ),
        explanation=_build_explanation(
            ranking_input.target_symbol,
            supporting_evidence=supporting_evidence,
            risk_evidence=risk_evidence,
        ),
        freshnessDays=ranking_input.freshness_days,
        confidenceLabel=ranking_input.confidence_label,
    )


def _calculate_safety_penalty(
    serious_event_count: int,
    warning_flag: bool,
    safety_multiplier: float,
) -> float:
    if serious_event_count >= 500:
        base_penalty = 30.0
    elif serious_event_count >= 100 or warning_flag:
        base_penalty = 15.0
    elif serious_event_count >= 25:
        base_penalty = 5.0
    else:
        base_penalty = 0.0
    return base_penalty * safety_multiplier


def _build_explanation(
    target_symbol: str,
    supporting_evidence: list[dict[str, object]],
    risk_evidence: list[dict[str, object]],
) -> Explanation:
    return Explanation(
        summary=(
            f"{target_symbol} ranks highly for ulcerative colitis because association, clinical, "
            "and chemical evidence converge despite a visible safety penalty."
        ),
        supportingEvidence=[
            EvidenceItem(
                source=item["source"],
                sourceRecordId=item["source_record_id"],
                title=item["title"],
                detail=item["detail"],
            )
            for item in supporting_evidence
        ],
        riskEvidence=[
            EvidenceItem(
                source=item["source"],
                sourceRecordId=item["source_record_id"],
                title=item["title"],
                detail=item["detail"],
            )
            for item in risk_evidence
        ],
    )


def _percentile_for_score(score: float) -> int:
    if score >= 65:
        return 99
    if score >= 55:
        return 94
    if score >= 45:
        return 88
    return 70


def _clamp(score: float) -> float:
    return max(0.0, min(100.0, score))
