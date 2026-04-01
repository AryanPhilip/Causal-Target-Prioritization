from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctpc.models.base import Base


class Target(Base):
    __tablename__ = "targets"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    symbol: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    evidence_rows = relationship(
        "DiseaseTargetEvidence", back_populates="target", cascade="all, delete-orphan"
    )
    compounds = relationship("TargetCompound", back_populates="target", cascade="all, delete-orphan")
    trials = relationship("TargetTrial", back_populates="target", cascade="all, delete-orphan")
    safety_signals = relationship(
        "SafetySignal", back_populates="target", cascade="all, delete-orphan"
    )


class DiseaseTargetEvidence(Base):
    """Per (disease, target) scored row — source of truth for ranking components."""

    __tablename__ = "disease_target_evidence"

    disease_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("diseases.id", ondelete="CASCADE"), primary_key=True
    )
    target_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("targets.id", ondelete="CASCADE"), primary_key=True
    )
    profile: Mapped[str] = mapped_column(String(32), primary_key=True, default="balanced")

    association_evidence: Mapped[float] = mapped_column(Float, nullable=False)
    clinical_support: Mapped[float] = mapped_column(Float, nullable=False)
    chemical_support: Mapped[float] = mapped_column(Float, nullable=False)
    tractability: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_modifier: Mapped[float] = mapped_column(Float, nullable=False)
    safety_penalty: Mapped[float] = mapped_column(Float, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    percentile: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_label: Mapped[str] = mapped_column(String(32), nullable=False)
    freshness_days: Mapped[float] = mapped_column(Float, nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    supporting_evidence: Mapped[list] = mapped_column(JSONB, nullable=False)
    risk_evidence: Mapped[list] = mapped_column(JSONB, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    disease = relationship("Disease", back_populates="evidence_rows")
    target = relationship("Target", back_populates="evidence_rows")


class TargetCompound(Base):
    __tablename__ = "target_compounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("targets.id", ondelete="CASCADE"), index=True
    )
    chembl_id: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    modality: Mapped[str] = mapped_column(String(64), nullable=False)

    target = relationship("Target", back_populates="compounds")


class TargetTrial(Base):
    __tablename__ = "target_trials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("targets.id", ondelete="CASCADE"), index=True
    )
    nct_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    phase: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)

    target = relationship("Target", back_populates="trials")


class SafetySignal(Base):
    __tablename__ = "safety_signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("targets.id", ondelete="CASCADE"), index=True
    )
    disease_id: Mapped[str | None] = mapped_column(
        String(64), ForeignKey("diseases.id", ondelete="SET NULL"), nullable=True
    )
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    ingredient: Mapped[str] = mapped_column(String(256), nullable=False)
    serious_event_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    warning_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)

    target = relationship("Target", back_populates="safety_signals")
