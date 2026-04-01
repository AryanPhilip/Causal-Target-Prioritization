from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class RankingProfile(str, Enum):
    BALANCED = "balanced"
    CONSERVATIVE = "conservative"
    INNOVATION = "innovation"


class EvidenceItem(BaseModel):
    source: str
    source_record_id: str = Field(alias="sourceRecordId")
    title: str
    detail: str

    model_config = ConfigDict(populate_by_name=True)


class Explanation(BaseModel):
    summary: str
    supporting_evidence: list[EvidenceItem] = Field(alias="supportingEvidence")
    risk_evidence: list[EvidenceItem] = Field(alias="riskEvidence")

    model_config = ConfigDict(populate_by_name=True)


class ScoreComponents(BaseModel):
    association_evidence: float = Field(alias="associationEvidence")
    clinical_support: float = Field(alias="clinicalSupport")
    chemical_support: float = Field(alias="chemicalSupport")
    tractability: float
    confidence_modifier: float = Field(alias="confidenceModifier")
    safety_penalty: float = Field(alias="safetyPenalty")

    model_config = ConfigDict(populate_by_name=True)


class TargetScorecard(BaseModel):
    target_id: str = Field(alias="targetId")
    target_symbol: str = Field(alias="targetSymbol")
    target_name: str = Field(alias="targetName")
    disease_id: str = Field(alias="diseaseId")
    disease_name: str = Field(alias="diseaseName")
    overall_score: float = Field(alias="overallScore")
    percentile: int
    profile: RankingProfile
    components: ScoreComponents
    explanation: Explanation
    freshness_days: int = Field(alias="freshnessDays")
    confidence_label: str = Field(alias="confidenceLabel")

    model_config = ConfigDict(populate_by_name=True)


class DiseaseSummary(BaseModel):
    id: str
    label: str
    synonyms: list[str]


class SourceStatus(BaseModel):
    source: str
    last_successful_ingest_at: str = Field(alias="lastSuccessfulIngestAt")
    freshness_hours: int = Field(alias="freshnessHours")
    row_count: int = Field(alias="rowCount")
    mapping_coverage: float = Field(alias="mappingCoverage")
    validation_status: str = Field(alias="validationStatus")

    model_config = ConfigDict(populate_by_name=True)


class CompoundSummary(BaseModel):
    chembl_id: str = Field(alias="chemblId")
    name: str
    modality: str

    model_config = ConfigDict(populate_by_name=True)


class ClinicalTrialSummary(BaseModel):
    nct_id: str = Field(alias="nctId")
    title: str
    phase: str
    status: str

    model_config = ConfigDict(populate_by_name=True)


class SafetySignalSummary(BaseModel):
    source: str
    ingredient: str
    serious_event_count: int = Field(alias="seriousEventCount")
    warning_flag: bool = Field(alias="warningFlag")
    detail: str

    model_config = ConfigDict(populate_by_name=True)


class TargetDetail(BaseModel):
    target_id: str = Field(alias="targetId")
    target_symbol: str = Field(alias="targetSymbol")
    target_name: str = Field(alias="targetName")
    disease_id: str = Field(alias="diseaseId")
    disease_name: str = Field(alias="diseaseName")
    scorecard: TargetScorecard
    linked_compounds: list[CompoundSummary] = Field(alias="linkedCompounds")
    linked_trials: list[ClinicalTrialSummary] = Field(alias="linkedTrials")
    safety_signals: list[SafetySignalSummary] = Field(alias="safetySignals")

    model_config = ConfigDict(populate_by_name=True)
