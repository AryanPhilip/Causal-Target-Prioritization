from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from ctpc.core.types import (
    ClinicalTrialSummary,
    CompoundSummary,
    DiseaseSummary,
    EvidenceItem,
    RankingProfile,
    SafetySignalSummary,
    SourceStatus,
    TargetDetail,
    TargetScorecard,
)
from ctpc.db.models import ClinicalTrial, Compound, Disease, EvidenceRecord, SafetySignal, SourceStatusRecord, Target, TargetRankingRecord
from ctpc.services.ranking import RankingInput, build_scorecard


def list_diseases(session: Session, query: str) -> list[DiseaseSummary]:
    statement = select(Disease)
    if query:
        statement = statement.where(Disease.label.ilike(f"%{query}%"))
    diseases = session.scalars(statement).all()
    return [DiseaseSummary(id=item.id, label=item.label, synonyms=item.synonyms) for item in diseases]


def ranked_targets(session: Session, disease_id: str, profile: RankingProfile) -> list[TargetScorecard]:
    disease = session.get(Disease, disease_id)
    if not disease:
        return []

    target_map = {
        item.id: item
        for item in session.scalars(select(Target)).all()
    }
    evidence_records = session.scalars(
        select(EvidenceRecord).where(EvidenceRecord.disease_id == disease_id)
    ).all()
    evidence_by_target = _group_evidence(evidence_records)

    ranking_records = session.scalars(
        select(TargetRankingRecord).where(TargetRankingRecord.disease_id == disease_id)
    ).all()
    scorecards = [
        build_scorecard(
            RankingInput(
                target_id=record.target_id,
                target_symbol=target_map[record.target_id].symbol,
                target_name=target_map[record.target_id].name,
                association_evidence=record.association_evidence,
                clinical_support=record.clinical_support,
                chemical_support=record.chemical_support,
                tractability=record.tractability,
                confidence_modifier=record.confidence_modifier,
                serious_event_count=record.serious_event_count,
                warning_flag=record.warning_flag,
                freshness_days=record.freshness_days,
                confidence_label=record.confidence_label,
            ),
            profile,
            disease_id=disease.id,
            disease_name=disease.label,
            supporting_evidence=evidence_by_target.get(record.target_id, {}).get("supporting", []),
            risk_evidence=evidence_by_target.get(record.target_id, {}).get("risk", []),
        )
        for record in ranking_records
    ]
    return sorted(scorecards, key=lambda item: item.overall_score, reverse=True)


def target_detail(session: Session, disease_id: str, target_id: str, profile: RankingProfile) -> TargetDetail | None:
    scorecards = ranked_targets(session, disease_id, profile)
    scorecard = next((item for item in scorecards if item.target_id == target_id), None)
    if not scorecard:
        return None

    compounds = session.scalars(select(Compound).where(Compound.target_id == target_id)).all()
    trials = session.scalars(
        select(ClinicalTrial).where(
            ClinicalTrial.target_id == target_id,
            ClinicalTrial.disease_id == disease_id,
        )
    ).all()
    safety_signals = session.scalars(
        select(SafetySignal).where(
            SafetySignal.target_id == target_id,
            SafetySignal.disease_id == disease_id,
        )
    ).all()
    return TargetDetail(
        targetId=scorecard.target_id,
        targetSymbol=scorecard.target_symbol,
        targetName=scorecard.target_name,
        diseaseId=scorecard.disease_id,
        diseaseName=scorecard.disease_name,
        scorecard=scorecard,
        linkedCompounds=[
            CompoundSummary(chemblId=item.id, name=item.name, modality=item.modality)
            for item in compounds
        ],
        linkedTrials=[
            ClinicalTrialSummary(nctId=item.nct_id, title=item.title, phase=item.phase, status=item.status)
            for item in trials
        ],
        safetySignals=[
            SafetySignalSummary(
                source=item.source,
                ingredient=item.ingredient,
                seriousEventCount=item.serious_event_count,
                warningFlag=item.warning_flag,
                detail=item.detail,
            )
            for item in safety_signals
        ],
    )


def target_evidence(session: Session, disease_id: str, target_id: str) -> dict[str, list[EvidenceItem]]:
    evidence_records = session.scalars(
        select(EvidenceRecord).where(
            EvidenceRecord.disease_id == disease_id,
            EvidenceRecord.target_id == target_id,
        )
    ).all()
    grouped = {"supportingEvidence": [], "riskEvidence": []}
    for record in evidence_records:
        item = EvidenceItem(
            source=record.source,
            sourceRecordId=record.source_record_id,
            title=record.title,
            detail=record.detail,
        )
        key = "supportingEvidence" if record.evidence_kind == "supporting" else "riskEvidence"
        grouped[key].append(item)
    return grouped


def compare_targets(
    session: Session,
    disease_id: str,
    target_ids: list[str],
    profile: RankingProfile,
) -> list[TargetScorecard]:
    scorecards = ranked_targets(session, disease_id, profile)
    requested = set(target_ids)
    return [item for item in scorecards if item.target_id in requested][:4]


def list_source_status(session: Session) -> list[SourceStatus]:
    items = session.scalars(select(SourceStatusRecord)).all()
    return [
        SourceStatus(
            source=item.source,
            lastSuccessfulIngestAt=item.last_successful_ingest_at.isoformat().replace("+00:00", "Z"),
            freshnessHours=item.freshness_hours,
            rowCount=item.row_count,
            mappingCoverage=item.mapping_coverage,
            validationStatus=item.validation_status,
        )
        for item in items
    ]


def _group_evidence(records: list[EvidenceRecord]) -> dict[str, dict[str, list[dict[str, object]]]]:
    grouped: dict[str, dict[str, list[dict[str, object]]]] = {}
    for record in records:
        bucket = grouped.setdefault(record.target_id, {"supporting": [], "risk": []})
        bucket[record.evidence_kind].append(
            {
                "source": record.source,
                "source_record_id": record.source_record_id,
                "title": record.title,
                "detail": record.detail,
            }
        )
    return grouped
