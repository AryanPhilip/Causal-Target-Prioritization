"""REST API v1 — matches frontend/lib/api.ts."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ctpc.db import get_db
from ctpc.models import (
    Disease,
    DiseaseTargetEvidence,
    SafetySignal,
    SourceState,
    Target,
    TargetCompound,
    TargetTrial,
)
from ctpc.schemas import (
    DiseaseSummary,
    LinkedCompound,
    LinkedTrial,
    SafetySignalOut,
    SourceStatus,
    TargetDetail,
    TargetScorecard,
)
from ctpc.services.scorecard import evidence_row_to_scorecard

router = APIRouter(prefix="/api/v1")


@router.get("/diseases")
def list_diseases(
    query: str = "ulcerative",
    db: Session = Depends(get_db),
) -> dict:
    stmt = select(Disease).where(Disease.label.ilike(f"%{query}%"))
    rows = db.scalars(stmt).all()
    if not rows:
        rows = db.scalars(select(Disease)).all()
    items = [
        DiseaseSummary(id=d.id, label=d.label, synonyms=list(d.synonyms or []))
        for d in rows
    ]
    return {"items": items}


@router.get("/diseases/{disease_id}/targets")
def ranked_targets(
    disease_id: str,
    profile: str = "balanced",
    db: Session = Depends(get_db),
) -> dict:
    stmt = (
        select(DiseaseTargetEvidence, Target, Disease)
        .join(Target, Target.id == DiseaseTargetEvidence.target_id)
        .join(Disease, Disease.id == DiseaseTargetEvidence.disease_id)
        .where(
            DiseaseTargetEvidence.disease_id == disease_id,
            DiseaseTargetEvidence.profile == profile,
        )
        .order_by(DiseaseTargetEvidence.overall_score.desc())
    )
    rows = db.execute(stmt).all()
    items: list[TargetScorecard] = []
    for ev, tgt, dis in rows:
        items.append(evidence_row_to_scorecard(ev, tgt, dis.label))
    return {"items": items}


@router.get("/targets/{target_id}")
def target_detail(
    target_id: str,
    disease_id: str = Query(..., alias="disease_id"),
    db: Session = Depends(get_db),
) -> TargetDetail:
    tgt = db.get(Target, target_id)
    if not tgt:
        raise HTTPException(status_code=404, detail="Target not found")
    dis = db.get(Disease, disease_id)
    if not dis:
        raise HTTPException(status_code=404, detail="Disease not found")
    stmt = select(DiseaseTargetEvidence).where(
        DiseaseTargetEvidence.disease_id == disease_id,
        DiseaseTargetEvidence.target_id == target_id,
        DiseaseTargetEvidence.profile == "balanced",
    )
    ev = db.scalars(stmt).first()
    if not ev:
        raise HTTPException(status_code=404, detail="No scorecard for this disease–target pair")

    scorecard = evidence_row_to_scorecard(ev, tgt, dis.label)

    comps = db.scalars(
        select(TargetCompound).where(TargetCompound.target_id == target_id).limit(50)
    ).all()
    trials = db.scalars(
        select(TargetTrial).where(TargetTrial.target_id == target_id).limit(50)
    ).all()
    safety = db.scalars(
        select(SafetySignal).where(
            SafetySignal.target_id == target_id,
            SafetySignal.disease_id == disease_id,
        )
    ).all()

    return TargetDetail(
        targetId=tgt.id,
        targetSymbol=tgt.symbol,
        targetName=tgt.name,
        diseaseId=dis.id,
        diseaseName=dis.label,
        scorecard=scorecard,
        linkedCompounds=[
            LinkedCompound(chemblId=c.chembl_id, name=c.name, modality=c.modality) for c in comps
        ],
        linkedTrials=[
            LinkedTrial(nctId=t.nct_id, title=t.title, phase=t.phase, status=t.status)
            for t in trials
        ],
        safetySignals=[
            SafetySignalOut(
                source=s.source,
                ingredient=s.ingredient,
                seriousEventCount=s.serious_event_count,
                warningFlag=s.warning_flag,
                detail=s.detail,
            )
            for s in safety
        ],
    )


@router.get("/compare")
def compare(
    disease_id: str = Query(..., alias="disease_id"),
    target_ids: list[str] = Query(default=[], alias="target_ids"),
    db: Session = Depends(get_db),
) -> dict:
    if not target_ids:
        return {"items": []}
    dis = db.get(Disease, disease_id)
    if not dis:
        raise HTTPException(status_code=404, detail="Disease not found")
    items: list[TargetScorecard] = []
    for tid in target_ids:
        tgt = db.get(Target, tid)
        if not tgt:
            continue
        stmt = select(DiseaseTargetEvidence).where(
            DiseaseTargetEvidence.disease_id == disease_id,
            DiseaseTargetEvidence.target_id == tid,
            DiseaseTargetEvidence.profile == "balanced",
        )
        ev = db.scalars(stmt).first()
        if ev:
            items.append(evidence_row_to_scorecard(ev, tgt, dis.label))
    return {"items": items}


@router.get("/admin/sources")
def admin_sources(db: Session = Depends(get_db)) -> dict:
    rows = db.scalars(select(SourceState)).all()
    now = datetime.now(tz=timezone.utc)
    items: list[SourceStatus] = []
    for s in rows:
        last = s.last_success_at or now
        hours = max(0.0, (now - last).total_seconds() / 3600.0)
        items.append(
            SourceStatus(
                source=s.source,
                lastSuccessfulIngestAt=last.isoformat().replace("+00:00", "Z"),
                freshnessHours=round(hours, 2),
                rowCount=s.row_count,
                mappingCoverage=round(s.mapping_coverage, 4),
                validationStatus=s.validation_status,
            )
        )
    if not items:
        for name in ("opentargets", "chembl", "clinicaltrials_gov"):
            items.append(
                SourceStatus(
                    source=name,
                    lastSuccessfulIngestAt=now.isoformat().replace("+00:00", "Z"),
                    freshnessHours=0.0,
                    rowCount=0,
                    mappingCoverage=1.0,
                    validationStatus="UNKNOWN",
                )
            )
    return {"items": items}
