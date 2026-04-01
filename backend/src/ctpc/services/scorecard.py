"""Map ORM rows to API scorecard payloads."""

from ctpc.models import DiseaseTargetEvidence, Target
from ctpc.schemas import (
    EvidenceItem,
    ExplanationBlock,
    ScoreComponents,
    TargetScorecard,
)


def evidence_row_to_scorecard(
    row: DiseaseTargetEvidence,
    target: Target,
    disease_label: str,
) -> TargetScorecard:
    sup = row.supporting_evidence or []
    risk = row.risk_evidence or []
    return TargetScorecard(
        targetId=target.id,
        targetSymbol=target.symbol,
        targetName=target.name,
        diseaseId=row.disease_id,
        diseaseName=disease_label,
        overallScore=round(row.overall_score, 2),
        percentile=round(row.percentile, 1),
        profile=row.profile,
        freshnessDays=round(row.freshness_days, 2),
        confidenceLabel=row.confidence_label,
        components=ScoreComponents(
            associationEvidence=round(row.association_evidence, 2),
            clinicalSupport=round(row.clinical_support, 2),
            chemicalSupport=round(row.chemical_support, 2),
            tractability=round(row.tractability, 2),
            confidenceModifier=round(row.confidence_modifier, 2),
            safetyPenalty=round(row.safety_penalty, 2),
        ),
        explanation=ExplanationBlock(
            summary=row.summary_text,
            supportingEvidence=[EvidenceItem(**x) for x in sup if isinstance(x, dict)],
            riskEvidence=[EvidenceItem(**x) for x in risk if isinstance(x, dict)],
        ),
    )
