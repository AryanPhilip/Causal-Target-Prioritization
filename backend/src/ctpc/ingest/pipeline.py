"""Orchestrate OpenTargets + ChEMBL + ClinicalTrials ingest into Postgres."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
import httpx
from sqlalchemy import delete, desc, func, select
from sqlalchemy.orm import Session

from ctpc.ingest import chembl, clinicaltrials, opentargets
from ctpc.ingest.disease_map import resolve_for_opentargets
from ctpc.models import (
    Disease,
    DiseaseTargetEvidence,
    IngestRun,
    SafetySignal,
    SourceState,
    Target,
    TargetCompound,
    TargetTrial,
)
from ctpc.services.ranking import (
    confidence_label_from_modifier,
    modifier_from_association,
    overall_score,
    percentiles_from_scores,
    safety_penalty_heuristic,
)

log = logging.getLogger(__name__)

SOURCES = ("opentargets", "chembl", "clinicaltrials_gov")


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def run_full_ingest(session: Session, *, disease_ids: list[str] | None = None) -> None:
    """Run ingest for configured diseases (default: MONDO UC)."""
    diseases = disease_ids or ["MONDO:0005101"]
    client = httpx.Client(timeout=120.0)
    try:
        for src in SOURCES:
            _start_run(session, src)
        for did in diseases:
            _ingest_disease_vertical(session, client, did)
        for src in SOURCES:
            _finish_run_ok(session, src)
    except Exception as e:
        log.exception("ingest failed: %s", e)
        for src in SOURCES:
            _finish_run_err(session, src, str(e))
        raise
    finally:
        client.close()


def _start_run(session: Session, source: str) -> None:
    session.add(
        IngestRun(
            source=source,
            started_at=_now(),
            status="running",
            rows_affected=0,
        )
    )
    session.commit()


def _finish_run_ok(session: Session, source: str) -> None:
    run = session.scalars(
        select(IngestRun)
        .where(IngestRun.source == source, IngestRun.status == "running")
        .order_by(desc(IngestRun.id))
        .limit(1)
    ).first()
    if run and run.status == "running":
        run.status = "ok"
        run.finished_at = _now()
    st = session.get(SourceState, source)
    if not st:
        st = SourceState(source=source)
        session.add(st)
    st.last_success_at = _now()
    st.validation_status = "OK"
    if source == "opentargets":
        st.row_count = int(session.scalar(select(func.count()).select_from(Target)) or 0)
    elif source == "chembl":
        st.row_count = int(session.scalar(select(func.count()).select_from(TargetCompound)) or 0)
    elif source == "clinicaltrials_gov":
        st.row_count = int(session.scalar(select(func.count()).select_from(TargetTrial)) or 0)
    session.commit()


def _finish_run_err(session: Session, source: str, msg: str) -> None:
    run = session.scalars(
        select(IngestRun)
        .where(IngestRun.source == source, IngestRun.status == "running")
        .order_by(desc(IngestRun.id))
        .limit(1)
    ).first()
    if run and run.status == "running":
        run.status = "error"
        run.finished_at = _now()
        run.error_message = msg[:5000]
    session.commit()


def _ingest_disease_vertical(session: Session, client: httpx.Client, mondo_id: str) -> None:
    ot_id = resolve_for_opentargets(mondo_id)
    _ot_id, dname, rows = opentargets.fetch_disease_associated_targets(mondo_id, limit=50, client=client)
    if not rows:
        log.warning("No associations for disease %s", mondo_id)
        return

    label = dname
    synonyms: list[str] = []
    if mondo_id == "MONDO:0005101":
        label = "ulcerative colitis"
        synonyms = ["UC", "inflammatory bowel disease"]

    session.merge(Disease(id=mondo_id, label=label, synonyms=synonyms))
    session.commit()

    # Take top targets by association score
    rows.sort(key=lambda x: x.association_score, reverse=True)
    top = rows[:25]

    # Clear previous evidence for this disease + profile
    session.execute(
        delete(DiseaseTargetEvidence).where(
            DiseaseTargetEvidence.disease_id == mondo_id,
            DiseaseTargetEvidence.profile == "balanced",
        )
    )
    tids = [t.ensembl_id for t in top]
    if tids:
        session.execute(delete(TargetCompound).where(TargetCompound.target_id.in_(tids)))
        session.execute(delete(TargetTrial).where(TargetTrial.target_id.in_(tids)))
        session.execute(delete(SafetySignal).where(SafetySignal.target_id.in_(tids)))
    session.commit()

    built: list[dict] = []
    for at in top:
        uni = opentargets.fetch_uniprot_swissprot(at.ensembl_id, client=client)
        ct = chembl.resolve_chembl_target_id(at.ensembl_id, uni, client=client)
        n_mech = chembl.count_mechanism_drugs(ct) if ct else 0
        compounds = chembl.fetch_top_compounds(ct, limit=5, client=client) if ct else []
        trials = clinicaltrials.search_trials_for_target(
            at.symbol, disease_terms="ulcerative colitis", page_size=25, client=client
        )
        trial_join = " ".join(t["title"] for t in trials)

        assoc = at.association_score * 100.0
        clin = clinicaltrials.clinical_support_score(len(trials))
        chem = chembl.chemical_support_score(n_mech)
        tract = opentargets.tractability_score(at.association_score)
        conf = modifier_from_association(at.association_score)
        safe = safety_penalty_heuristic(trial_join, len(trials))

        sc = overall_score(assoc, clin, chem, tract, conf, safe)

        session.merge(
            Target(
                id=at.ensembl_id,
                symbol=at.symbol,
                name=at.name,
            )
        )
        for comp in compounds:
            session.add(
                TargetCompound(
                    target_id=at.ensembl_id,
                    chembl_id=comp["chemblId"],
                    name=comp["name"],
                    modality=comp["modality"],
                )
            )
        for tr in trials[:15]:
            session.add(
                TargetTrial(
                    target_id=at.ensembl_id,
                    nct_id=tr["nctId"],
                    title=tr["title"],
                    phase=tr["phase"],
                    status=tr["status"],
                )
            )
        warn = safe > 28.0
        session.add(
            SafetySignal(
                target_id=at.ensembl_id,
                disease_id=mondo_id,
                source="heuristic",
                ingredient=at.symbol,
                serious_event_count=min(100, int(safe)),
                warning_flag=warn,
                detail="Inferred burden from trial volume and keyword scan (not a substitute for FAERS).",
            )
        )

        sup_ev = [
            {
                "source": "OpenTargets",
                "sourceRecordId": ot_id,
                "title": "Genetic association evidence",
                "detail": f"Overall association score {at.association_score:.3f} for {label}.",
            },
            {
                "source": "ClinicalTrials.gov",
                "sourceRecordId": trials[0]["nctId"] if trials else "n/a",
                "title": "Clinical trial coverage",
                "detail": f"{len(trials)} UC-related trials mentioning {at.symbol}.",
            },
        ]
        risk_ev = []
        if warn:
            risk_ev.append(
                {
                    "source": "CTPC",
                    "sourceRecordId": "safety-heuristic",
                    "title": "Safety heuristic",
                    "detail": "Elevated penalty from trial metadata heuristics; see pharmacovigilance sources for decisions.",
                }
            )

        summary = (
            f"{at.symbol} ranks for {label} with converging association and clinical signals; "
            f"safety penalty is {safe:.1f} on a 0–100 scale."
        )

        built.append(
            {
                "at": at,
                "assoc": assoc,
                "clin": clin,
                "chem": chem,
                "tract": tract,
                "conf": conf,
                "safe": safe,
                "score": sc,
                "summary": summary,
                "supporting": sup_ev,
                "risk": risk_ev,
            }
        )

    session.commit()

    scores = [b["score"] for b in built]
    pcts = percentiles_from_scores(scores)
    now = _now()
    for i, b in enumerate(built):
        at = b["at"]
        session.add(
            DiseaseTargetEvidence(
                disease_id=mondo_id,
                target_id=at.ensembl_id,
                profile="balanced",
                association_evidence=b["assoc"],
                clinical_support=b["clin"],
                chemical_support=b["chem"],
                tractability=b["tract"],
                confidence_modifier=b["conf"],
                safety_penalty=b["safe"],
                overall_score=b["score"],
                percentile=pcts[i],
                confidence_label=confidence_label_from_modifier(b["conf"]),
                freshness_days=0.0,
                summary_text=b["summary"],
                supporting_evidence=b["supporting"],
                risk_evidence=b["risk"],
                updated_at=now,
            )
        )
    session.commit()
