from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from strawberry.fastapi import GraphQLRouter

from ctpc.api.schema import schema
from ctpc.core.types import RankingProfile
from ctpc.db.models import TargetRankingRecord
from ctpc.db.session import DatabaseManager
from ctpc.ingest.pipeline import ingest_all_sources
from ctpc.services.query import compare_targets, list_diseases, list_source_status, ranked_targets, target_detail, target_evidence


def create_app(manager: DatabaseManager | None = None, seed_demo_data: bool = True) -> FastAPI:
    db_manager = manager or DatabaseManager.for_memory()
    db_manager.create_all()
    if seed_demo_data:
        with db_manager.session() as session:
            has_seed_data = session.query(TargetRankingRecord).first() is not None
        if not has_seed_data:
            ingest_all_sources(db_manager)

    app = FastAPI(title="CTPC API", version="0.1.0")
    app.state.db_manager = db_manager

    @app.get("/healthz")
    def healthcheck() -> dict[str, str]:
        return {"service": "ctpc-backend", "status": "ok"}

    @app.get("/api/v1/diseases")
    def search_diseases(query: str = Query("")) -> dict[str, list[dict[str, object]]]:
        with db_manager.session() as session:
            items = list_diseases(session, query)
        return {"items": [item.model_dump() for item in items]}

    @app.get("/api/v1/diseases/{disease_id}/targets")
    def get_ranked_targets(
        disease_id: str,
        profile: RankingProfile = RankingProfile.BALANCED,
        limit: int = 10,
    ) -> dict[str, list[dict[str, object]]]:
        with db_manager.session() as session:
            scorecards = ranked_targets(session, disease_id, profile)[:limit]
        return {"items": [item.model_dump(by_alias=True) for item in scorecards]}

    @app.get("/api/v1/targets/{target_id}")
    def get_target_detail(
        target_id: str,
        disease_id: str,
        profile: RankingProfile = RankingProfile.BALANCED,
    ) -> dict[str, object]:
        with db_manager.session() as session:
            detail = target_detail(session, disease_id, target_id, profile)
        if not detail:
            raise HTTPException(status_code=404, detail="Target not found")
        return detail.model_dump(by_alias=True)

    @app.get("/api/v1/targets/{target_id}/evidence")
    def get_target_evidence(target_id: str, disease_id: str) -> dict[str, list[dict[str, object]]]:
        with db_manager.session() as session:
            evidence = target_evidence(session, disease_id, target_id)
        return {
            key: [item.model_dump(by_alias=True) for item in items]
            for key, items in evidence.items()
        }

    @app.get("/api/v1/compare")
    def get_target_comparison(
        disease_id: str,
        target_ids: list[str] = Query(...),
        profile: RankingProfile = RankingProfile.BALANCED,
    ) -> dict[str, list[dict[str, object]]]:
        with db_manager.session() as session:
            items = compare_targets(session, disease_id, target_ids, profile)
        return {"items": [item.model_dump(by_alias=True) for item in items]}

    @app.get("/api/v1/admin/sources")
    def get_source_status() -> dict[str, list[dict[str, object]]]:
        with db_manager.session() as session:
            items = list_source_status(session)
        return {"items": [item.model_dump(by_alias=True) for item in items]}

    @app.post("/api/v1/admin/ingest/{source}")
    def ingest_source(source: str) -> dict[str, int | str]:
        return ingest_all_sources(db_manager, source_name=source)

    app.include_router(GraphQLRouter(schema, context_getter=lambda: {"db_manager": db_manager}), prefix="/graphql")
    return app
