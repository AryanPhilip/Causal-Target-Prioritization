from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SourceDataset(Base):
    __tablename__ = "source_dataset"
    __table_args__ = {"schema": "core"}

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    label: Mapped[str] = mapped_column(String(128))
    dataset_version: Mapped[str] = mapped_column(String(64))
    provenance_url: Mapped[str] = mapped_column(String(256))


class Disease(Base):
    __tablename__ = "disease"
    __table_args__ = {"schema": "core"}

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    label: Mapped[str] = mapped_column(String(256))
    synonyms: Mapped[list[str]] = mapped_column(JSON)


class Target(Base):
    __tablename__ = "target"
    __table_args__ = {"schema": "core"}

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    symbol: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(256))


class Compound(Base):
    __tablename__ = "compound"
    __table_args__ = {"schema": "core"}

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    target_id: Mapped[str] = mapped_column(ForeignKey("core.target.id"), index=True)
    name: Mapped[str] = mapped_column(String(128))
    modality: Mapped[str] = mapped_column(String(64))


class ClinicalTrial(Base):
    __tablename__ = "clinical_trial"
    __table_args__ = {"schema": "core"}

    nct_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    target_id: Mapped[str] = mapped_column(ForeignKey("core.target.id"), index=True)
    disease_id: Mapped[str] = mapped_column(ForeignKey("core.disease.id"), index=True)
    title: Mapped[str] = mapped_column(String(256))
    phase: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(64))


class SafetySignal(Base):
    __tablename__ = "safety_signal"
    __table_args__ = {"schema": "core"}

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    target_id: Mapped[str] = mapped_column(ForeignKey("core.target.id"), index=True)
    disease_id: Mapped[str] = mapped_column(ForeignKey("core.disease.id"), index=True)
    source: Mapped[str] = mapped_column(String(64))
    ingredient: Mapped[str] = mapped_column(String(128))
    serious_event_count: Mapped[int] = mapped_column(Integer)
    warning_flag: Mapped[bool] = mapped_column(Boolean)
    detail: Mapped[str] = mapped_column(Text)


class EvidenceRecord(Base):
    __tablename__ = "evidence_record"
    __table_args__ = (
        UniqueConstraint("source", "source_record_id"),
        {"schema": "core"},
    )

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    target_id: Mapped[str] = mapped_column(ForeignKey("core.target.id"), index=True)
    disease_id: Mapped[str] = mapped_column(ForeignKey("core.disease.id"), index=True)
    source: Mapped[str] = mapped_column(String(64), index=True)
    source_record_id: Mapped[str] = mapped_column(String(128))
    evidence_kind: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(256))
    detail: Mapped[str] = mapped_column(Text)


class MappingRecord(Base):
    __tablename__ = "mapping_record"
    __table_args__ = {"schema": "core"}

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    source: Mapped[str] = mapped_column(String(64))
    entity_type: Mapped[str] = mapped_column(String(64))
    source_value: Mapped[str] = mapped_column(String(128))
    canonical_id: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32))


class TargetRankingRecord(Base):
    __tablename__ = "target_ranking"
    __table_args__ = (
        UniqueConstraint("disease_id", "target_id"),
        {"schema": "marts"},
    )

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    disease_id: Mapped[str] = mapped_column(ForeignKey("core.disease.id"), index=True)
    target_id: Mapped[str] = mapped_column(ForeignKey("core.target.id"), index=True)
    association_evidence: Mapped[float] = mapped_column(Float)
    clinical_support: Mapped[float] = mapped_column(Float)
    chemical_support: Mapped[float] = mapped_column(Float)
    tractability: Mapped[float] = mapped_column(Float)
    confidence_modifier: Mapped[float] = mapped_column(Float)
    serious_event_count: Mapped[int] = mapped_column(Integer)
    warning_flag: Mapped[bool] = mapped_column(Boolean)
    freshness_days: Mapped[int] = mapped_column(Integer)
    confidence_label: Mapped[str] = mapped_column(String(32))


class IngestRun(Base):
    __tablename__ = "ingest_run"
    __table_args__ = {"schema": "raw"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(64), index=True)
    dataset_version: Mapped[str] = mapped_column(String(64))
    checksum: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32))
    rows_loaded: Mapped[int] = mapped_column(Integer)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SourcePayload(Base):
    __tablename__ = "source_payload"
    __table_args__ = (
        UniqueConstraint("source", "source_record_id", "dataset_version"),
        {"schema": "raw"},
    )

    id: Mapped[str] = mapped_column(String(160), primary_key=True)
    source: Mapped[str] = mapped_column(String(64))
    dataset_version: Mapped[str] = mapped_column(String(64))
    source_record_id: Mapped[str] = mapped_column(String(128))
    payload: Mapped[dict[str, object]] = mapped_column(JSON)


class ValidationResult(Base):
    __tablename__ = "validation_result"
    __table_args__ = {"schema": "ops"}

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    source: Mapped[str] = mapped_column(String(64), index=True)
    check_name: Mapped[str] = mapped_column(String(64))
    severity: Mapped[str] = mapped_column(String(32))
    message: Mapped[str] = mapped_column(String(256))


class SourceStatusRecord(Base):
    __tablename__ = "source_status"
    __table_args__ = {"schema": "ops"}

    source: Mapped[str] = mapped_column(String(64), primary_key=True)
    last_successful_ingest_at: Mapped[datetime] = mapped_column(DateTime)
    freshness_hours: Mapped[int] = mapped_column(Integer)
    row_count: Mapped[int] = mapped_column(Integer)
    mapping_coverage: Mapped[float] = mapped_column(Float)
    validation_status: Mapped[str] = mapped_column(String(32))
