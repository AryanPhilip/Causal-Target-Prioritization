"""Pydantic models aligned with frontend/lib/types.ts."""

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    source: str
    sourceRecordId: str
    title: str
    detail: str


class ScoreComponents(BaseModel):
    associationEvidence: float
    clinicalSupport: float
    chemicalSupport: float
    tractability: float
    confidenceModifier: float
    safetyPenalty: float


class ExplanationBlock(BaseModel):
    summary: str
    supportingEvidence: list[EvidenceItem] = Field(default_factory=list)
    riskEvidence: list[EvidenceItem] = Field(default_factory=list)


class TargetScorecard(BaseModel):
    targetId: str
    targetSymbol: str
    targetName: str
    diseaseId: str
    diseaseName: str
    overallScore: float
    percentile: float
    profile: str
    freshnessDays: float
    confidenceLabel: str
    components: ScoreComponents
    explanation: ExplanationBlock


class SourceStatus(BaseModel):
    source: str
    lastSuccessfulIngestAt: str
    freshnessHours: float
    rowCount: int
    mappingCoverage: float
    validationStatus: str


class DiseaseSummary(BaseModel):
    id: str
    label: str
    synonyms: list[str]


class LinkedCompound(BaseModel):
    chemblId: str
    name: str
    modality: str


class LinkedTrial(BaseModel):
    nctId: str
    title: str
    phase: str
    status: str


class SafetySignalOut(BaseModel):
    source: str
    ingredient: str
    seriousEventCount: int
    warningFlag: bool
    detail: str


class TargetDetail(BaseModel):
    targetId: str
    targetSymbol: str
    targetName: str
    diseaseId: str
    diseaseName: str
    scorecard: TargetScorecard
    linkedCompounds: list[LinkedCompound]
    linkedTrials: list[LinkedTrial]
    safetySignals: list[SafetySignalOut]
