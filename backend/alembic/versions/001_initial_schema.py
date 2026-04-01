"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-03-30

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "diseases",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("label", sa.Text(), nullable=False),
        sa.Column(
            "synonyms",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "targets",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_targets_symbol"), "targets", ["symbol"], unique=False)

    op.create_table(
        "source_states",
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("last_success_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("mapping_coverage", sa.Float(), nullable=False),
        sa.Column("validation_status", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("source"),
    )

    op.create_table(
        "ingest_runs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("rows_affected", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ingest_runs_source"), "ingest_runs", ["source"], unique=False)

    op.create_table(
        "disease_target_evidence",
        sa.Column("disease_id", sa.String(length=64), nullable=False),
        sa.Column("target_id", sa.String(length=64), nullable=False),
        sa.Column("profile", sa.String(length=32), nullable=False),
        sa.Column("association_evidence", sa.Float(), nullable=False),
        sa.Column("clinical_support", sa.Float(), nullable=False),
        sa.Column("chemical_support", sa.Float(), nullable=False),
        sa.Column("tractability", sa.Float(), nullable=False),
        sa.Column("confidence_modifier", sa.Float(), nullable=False),
        sa.Column("safety_penalty", sa.Float(), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("percentile", sa.Float(), nullable=False),
        sa.Column("confidence_label", sa.String(length=32), nullable=False),
        sa.Column("freshness_days", sa.Float(), nullable=False),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("supporting_evidence", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("risk_evidence", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["disease_id"], ["diseases.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_id"], ["targets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("disease_id", "target_id", "profile"),
    )

    op.create_table(
        "target_compounds",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("target_id", sa.String(length=64), nullable=False),
        sa.Column("chembl_id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("modality", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["target_id"], ["targets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_target_compounds_target_id"), "target_compounds", ["target_id"], unique=False)

    op.create_table(
        "target_trials",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("target_id", sa.String(length=64), nullable=False),
        sa.Column("nct_id", sa.String(length=32), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("phase", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["target_id"], ["targets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_target_trials_target_id"), "target_trials", ["target_id"], unique=False)
    op.create_index(op.f("ix_target_trials_nct_id"), "target_trials", ["nct_id"], unique=False)

    op.create_table(
        "safety_signals",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("target_id", sa.String(length=64), nullable=False),
        sa.Column("disease_id", sa.String(length=64), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("ingredient", sa.String(length=256), nullable=False),
        sa.Column("serious_event_count", sa.Integer(), nullable=False),
        sa.Column("warning_flag", sa.Boolean(), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["disease_id"], ["diseases.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["target_id"], ["targets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_safety_signals_target_id"), "safety_signals", ["target_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_safety_signals_target_id"), table_name="safety_signals")
    op.drop_table("safety_signals")
    op.drop_index(op.f("ix_target_trials_nct_id"), table_name="target_trials")
    op.drop_index(op.f("ix_target_trials_target_id"), table_name="target_trials")
    op.drop_table("target_trials")
    op.drop_index(op.f("ix_target_compounds_target_id"), table_name="target_compounds")
    op.drop_table("target_compounds")
    op.drop_table("disease_target_evidence")
    op.drop_index(op.f("ix_ingest_runs_source"), table_name="ingest_runs")
    op.drop_table("ingest_runs")
    op.drop_table("source_states")
    op.drop_index(op.f("ix_targets_symbol"), table_name="targets")
    op.drop_table("targets")
    op.drop_table("diseases")
