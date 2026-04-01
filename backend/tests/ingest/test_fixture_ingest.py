from pathlib import Path

from sqlalchemy import func, select

from ctpc.db.models import (
    Disease,
    EvidenceRecord,
    IngestRun,
    SourceStatusRecord,
    Target,
    TargetRankingRecord,
)
from ctpc.db.session import DatabaseManager
from ctpc.ingest.pipeline import ingest_all_sources


def test_fixture_ingest_is_idempotent_for_canonical_tables(tmp_path: Path) -> None:
    manager = DatabaseManager.for_sqlite(tmp_path / "ctpc.db")
    manager.create_all()

    ingest_all_sources(manager, source_name=None)
    ingest_all_sources(manager, source_name=None)

    with manager.session() as session:
        assert session.scalar(select(func.count(Disease.id))) == 1
        assert session.scalar(select(func.count(Target.id))) == 3
        assert session.scalar(select(func.count(EvidenceRecord.id))) == 9
        assert session.scalar(select(func.count(TargetRankingRecord.id))) == 3
        assert session.scalar(select(func.count(SourceStatusRecord.source))) == 4
        assert session.scalar(select(func.count(IngestRun.id))) == 8
