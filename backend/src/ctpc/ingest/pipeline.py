from __future__ import annotations

from datetime import UTC, datetime
from hashlib import sha256

from sqlalchemy import select

from ctpc.data.fixtures import RANKING_FIXTURES, SOURCE_STATUS_FIXTURES, UC_DISEASE
from ctpc.db.models import (
    ClinicalTrial,
    Compound,
    Disease,
    EvidenceRecord,
    IngestRun,
    MappingRecord,
    SafetySignal,
    SourceDataset,
    SourcePayload,
    SourceStatusRecord,
    Target,
    TargetRankingRecord,
    ValidationResult,
)
from ctpc.db.session import DatabaseManager


SOURCE_METADATA = {
    "opentargets": {
        "label": "Open Targets Platform",
        "dataset_version": "25.03",
        "provenance_url": "https://platform-docs.opentargets.org/",
    },
    "chembl": {
        "label": "ChEMBL",
        "dataset_version": "35",
        "provenance_url": "https://www.ebi.ac.uk/chembl/",
    },
    "clinicaltrials": {
        "label": "ClinicalTrials.gov API",
        "dataset_version": "v2",
        "provenance_url": "https://clinicaltrials.gov/data-api/about-api",
    },
    "openfda": {
        "label": "openFDA Drug Event",
        "dataset_version": "2025-Q4",
        "provenance_url": "https://open.fda.gov/apis/drug/event/",
    },
}


def ingest_all_sources(manager: DatabaseManager, source_name: str | None = None) -> dict[str, int | str]:
    sources = [source_name] if source_name else list(SOURCE_METADATA)
    total_rows = 0
    with manager.session() as session:
        _upsert_base_entities(session)
        session.flush()
        for source in sources:
            rows_loaded = _upsert_source(session, source)
            total_rows += rows_loaded
    return {"source": source_name or "all", "rowsLoaded": total_rows}


def _upsert_base_entities(session) -> None:  # type: ignore[no-untyped-def]
    session.merge(
        Disease(
            id=UC_DISEASE.id,
            label=UC_DISEASE.label,
            synonyms=UC_DISEASE.synonyms,
        )
    )
    for target in RANKING_FIXTURES:
        session.merge(
            Target(
                id=target["target_id"],
                symbol=target["target_symbol"],
                name=target["target_name"],
            )
        )


def _upsert_source(session, source: str) -> int:  # type: ignore[no-untyped-def]
    metadata = SOURCE_METADATA[source]
    session.merge(
        SourceDataset(
            id=source,
            label=metadata["label"],
            dataset_version=metadata["dataset_version"],
            provenance_url=metadata["provenance_url"],
        )
    )

    rows_loaded = 0
    for target in RANKING_FIXTURES:
        rows_loaded += _load_target_source_records(session, source, target, metadata["dataset_version"])

    status_fixture = next(item for item in SOURCE_STATUS_FIXTURES if item["source"] == source)
    session.merge(
        SourceStatusRecord(
            source=source,
            last_successful_ingest_at=datetime.fromisoformat(
                status_fixture["last_successful_ingest_at"].replace("Z", "+00:00")
            ),
            freshness_hours=status_fixture["freshness_hours"],
            row_count=status_fixture["row_count"],
            mapping_coverage=status_fixture["mapping_coverage"],
            validation_status=status_fixture["validation_status"],
        )
    )
    session.merge(
        ValidationResult(
            id=f"{source}:required-ids",
            source=source,
            check_name="required_ids",
            severity="warning" if status_fixture["validation_status"] == "warning" else "info",
            message=f"{source} mapping coverage is {status_fixture['mapping_coverage']:.0%}",
        )
    )

    run = IngestRun(
        source=source,
        dataset_version=metadata["dataset_version"],
        checksum=_checksum(source, metadata["dataset_version"], rows_loaded),
        status="completed",
        rows_loaded=rows_loaded,
        started_at=datetime.now(UTC),
        finished_at=datetime.now(UTC),
    )
    session.add(run)
    return rows_loaded


def _load_target_source_records(session, source: str, target: dict[str, object], dataset_version: str) -> int:  # type: ignore[no-untyped-def]
    target_id = str(target["target_id"])
    rows_loaded = 0

    session.merge(
        MappingRecord(
            id=f"{source}:{target_id}",
            source=source,
            entity_type="target",
            source_value=str(target["target_symbol"]),
            canonical_id=target_id,
            status="mapped",
        )
    )

    if source == "opentargets":
        session.merge(
            TargetRankingRecord(
                id=f"{UC_DISEASE.id}:{target_id}",
                disease_id=UC_DISEASE.id,
                target_id=target_id,
                association_evidence=float(target["association_evidence"]),
                clinical_support=float(target["clinical_support"]),
                chemical_support=float(target["chemical_support"]),
                tractability=float(target["tractability"]),
                confidence_modifier=float(target["confidence_modifier"]),
                serious_event_count=int(target["serious_event_count"]),
                warning_flag=bool(target["warning_flag"]),
                freshness_days=2,
                confidence_label="high" if float(target["confidence_modifier"]) >= 3 else "medium",
            )
        )
        for evidence in target["supporting_evidence"]:
            if evidence["source"] != "opentargets":
                continue
            _upsert_evidence(session, target_id, evidence, "supporting", dataset_version)
            rows_loaded += 1

    if source == "chembl":
        for compound in target["linked_compounds"]:
            session.merge(
                Compound(
                    id=compound["chembl_id"],
                    target_id=target_id,
                    name=compound["name"],
                    modality=compound["modality"],
                )
            )
            _upsert_payload(session, source, dataset_version, compound["chembl_id"], compound)
            rows_loaded += 1
        for evidence in target["supporting_evidence"]:
            if evidence["source"] != "chembl":
                continue
            _upsert_evidence(session, target_id, evidence, "supporting", dataset_version)
            rows_loaded += 1

    if source == "clinicaltrials":
        for trial in target["linked_trials"]:
            session.merge(
                ClinicalTrial(
                    nct_id=trial["nct_id"],
                    target_id=target_id,
                    disease_id=UC_DISEASE.id,
                    title=trial["title"],
                    phase=trial["phase"],
                    status=trial["status"],
                )
            )
            _upsert_payload(session, source, dataset_version, trial["nct_id"], trial)
            rows_loaded += 1
        for evidence in target["supporting_evidence"]:
            if evidence["source"] != "clinicaltrials":
                continue
            _upsert_evidence(session, target_id, evidence, "supporting", dataset_version)
            rows_loaded += 1

    if source == "openfda":
        for signal in target["safety_signals"]:
            signal_id = f"{target_id}:{signal['ingredient']}"
            session.merge(
                SafetySignal(
                    id=signal_id,
                    target_id=target_id,
                    disease_id=UC_DISEASE.id,
                    source=signal["source"],
                    ingredient=signal["ingredient"],
                    serious_event_count=signal["serious_event_count"],
                    warning_flag=signal["warning_flag"],
                    detail=signal["detail"],
                )
            )
            _upsert_payload(session, source, dataset_version, signal_id, signal)
            rows_loaded += 1
        for evidence in target["risk_evidence"]:
            _upsert_evidence(session, target_id, evidence, "risk", dataset_version)
            rows_loaded += 1

    return rows_loaded


def _upsert_evidence(session, target_id: str, evidence: dict[str, object], evidence_kind: str, dataset_version: str) -> None:  # type: ignore[no-untyped-def]
    evidence_id = f"{evidence['source']}:{evidence['source_record_id']}"
    session.merge(
        EvidenceRecord(
            id=evidence_id,
            target_id=target_id,
            disease_id=UC_DISEASE.id,
            source=evidence["source"],
            source_record_id=evidence["source_record_id"],
            evidence_kind=evidence_kind,
            title=evidence["title"],
            detail=evidence["detail"],
        )
    )
    _upsert_payload(session, evidence["source"], dataset_version, evidence["source_record_id"], evidence)


def _upsert_payload(session, source: str, dataset_version: str, source_record_id: str, payload: dict[str, object]) -> None:  # type: ignore[no-untyped-def]
    payload_id = f"{source}:{source_record_id}:{dataset_version}"
    for pending in session.new:
        if isinstance(pending, SourcePayload) and pending.id == payload_id:
            pending.payload = payload
            pending.source = source
            pending.dataset_version = dataset_version
            pending.source_record_id = source_record_id
            return
    existing = session.get(SourcePayload, payload_id)
    if existing:
        existing.payload = payload
        existing.source = source
        existing.dataset_version = dataset_version
        existing.source_record_id = source_record_id
        return
    session.add(
        SourcePayload(
            id=payload_id,
            source=source,
            dataset_version=dataset_version,
            source_record_id=source_record_id,
            payload=payload,
        )
    )


def _checksum(source: str, dataset_version: str, rows_loaded: int) -> str:
    digest = sha256(f"{source}:{dataset_version}:{rows_loaded}".encode("utf-8"))
    return digest.hexdigest()
