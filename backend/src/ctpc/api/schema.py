from __future__ import annotations

import strawberry

from ctpc.core.types import RankingProfile
from ctpc.db.session import DatabaseManager
from ctpc.services.query import compare_targets, list_diseases, list_source_status, ranked_targets, target_detail


@strawberry.type
class GraphQLEvidenceItem:
    source: str
    source_record_id: str
    title: str
    detail: str


@strawberry.type
class GraphQLExplanation:
    summary: str
    supporting_evidence: list[GraphQLEvidenceItem]
    risk_evidence: list[GraphQLEvidenceItem]


@strawberry.type
class GraphQLScoreComponents:
    association_evidence: float
    clinical_support: float
    chemical_support: float
    tractability: float
    confidence_modifier: float
    safety_penalty: float


@strawberry.type
class GraphQLTrial:
    nct_id: str
    title: str
    phase: str
    status: str


@strawberry.type
class GraphQLCompound:
    chembl_id: str
    name: str
    modality: str


@strawberry.type
class GraphQLSafetySignal:
    source: str
    ingredient: str
    serious_event_count: int
    warning_flag: bool
    detail: str


@strawberry.type
class GraphQLTargetScorecard:
    target_id: str
    target_symbol: str
    target_name: str
    disease_id: str
    disease_name: str
    overall_score: float
    percentile: int
    freshness_days: int
    confidence_label: str
    components: GraphQLScoreComponents
    explanation: GraphQLExplanation


@strawberry.type
class GraphQLTargetDetail:
    target_id: str
    target_symbol: str
    target_name: str
    disease_id: str
    disease_name: str
    linked_trials: list[GraphQLTrial]
    linked_compounds: list[GraphQLCompound]
    safety_signals: list[GraphQLSafetySignal]
    scorecard: GraphQLTargetScorecard


@strawberry.type
class GraphQLDisease:
    id: str
    label: str
    synonyms: list[str]


@strawberry.type
class GraphQLSourceStatus:
    source: str
    last_successful_ingest_at: str
    freshness_hours: int
    row_count: int
    mapping_coverage: float
    validation_status: str


def _scorecard_type(item: object) -> GraphQLTargetScorecard:
    return GraphQLTargetScorecard(
        target_id=item.target_id,
        target_symbol=item.target_symbol,
        target_name=item.target_name,
        disease_id=item.disease_id,
        disease_name=item.disease_name,
        overall_score=item.overall_score,
        percentile=item.percentile,
        freshness_days=item.freshness_days,
        confidence_label=item.confidence_label,
        components=GraphQLScoreComponents(
            association_evidence=item.components.association_evidence,
            clinical_support=item.components.clinical_support,
            chemical_support=item.components.chemical_support,
            tractability=item.components.tractability,
            confidence_modifier=item.components.confidence_modifier,
            safety_penalty=item.components.safety_penalty,
        ),
        explanation=GraphQLExplanation(
            summary=item.explanation.summary,
            supporting_evidence=[
                GraphQLEvidenceItem(
                    source=evidence.source,
                    source_record_id=evidence.source_record_id,
                    title=evidence.title,
                    detail=evidence.detail,
                )
                for evidence in item.explanation.supporting_evidence
            ],
            risk_evidence=[
                GraphQLEvidenceItem(
                    source=evidence.source,
                    source_record_id=evidence.source_record_id,
                    title=evidence.title,
                    detail=evidence.detail,
                )
                for evidence in item.explanation.risk_evidence
            ],
        ),
    )


@strawberry.type
class Query:
    @strawberry.field
    def disease_search(self, info: strawberry.Info, query: str) -> list[GraphQLDisease]:
        manager: DatabaseManager = info.context["db_manager"]
        with manager.session() as session:
            diseases = list_diseases(session, query)
        return [GraphQLDisease(**item.model_dump()) for item in diseases]

    @strawberry.field
    def ranked_targets(
        self,
        info: strawberry.Info,
        disease_id: str,
        profile: RankingProfile = RankingProfile.BALANCED,
    ) -> list[GraphQLTargetScorecard]:
        manager: DatabaseManager = info.context["db_manager"]
        with manager.session() as session:
            scorecards = ranked_targets(session, disease_id, profile)
        return [_scorecard_type(item) for item in scorecards]

    @strawberry.field
    def target(
        self,
        info: strawberry.Info,
        target_id: str,
        disease_id: str,
        profile: RankingProfile = RankingProfile.BALANCED,
    ) -> GraphQLTargetDetail | None:
        manager: DatabaseManager = info.context["db_manager"]
        with manager.session() as session:
            detail = target_detail(session, disease_id, target_id, profile)
        if not detail:
            return None
        return GraphQLTargetDetail(
            target_id=detail.target_id,
            target_symbol=detail.target_symbol,
            target_name=detail.target_name,
            disease_id=detail.disease_id,
            disease_name=detail.disease_name,
            linked_trials=[
                GraphQLTrial(
                    nct_id=item.nct_id,
                    title=item.title,
                    phase=item.phase,
                    status=item.status,
                )
                for item in detail.linked_trials
            ],
            linked_compounds=[
                GraphQLCompound(
                    chembl_id=item.chembl_id,
                    name=item.name,
                    modality=item.modality,
                )
                for item in detail.linked_compounds
            ],
            safety_signals=[
                GraphQLSafetySignal(
                    source=item.source,
                    ingredient=item.ingredient,
                    serious_event_count=item.serious_event_count,
                    warning_flag=item.warning_flag,
                    detail=item.detail,
                )
                for item in detail.safety_signals
            ],
            scorecard=_scorecard_type(detail.scorecard),
        )

    @strawberry.field
    def compare_targets(
        self,
        info: strawberry.Info,
        disease_id: str,
        target_ids: list[str],
        profile: RankingProfile = RankingProfile.BALANCED,
    ) -> list[GraphQLTargetScorecard]:
        manager: DatabaseManager = info.context["db_manager"]
        with manager.session() as session:
            scorecards = compare_targets(session, disease_id, target_ids, profile)
        return [_scorecard_type(item) for item in scorecards]

    @strawberry.field
    def source_status(self, info: strawberry.Info) -> list[GraphQLSourceStatus]:
        manager: DatabaseManager = info.context["db_manager"]
        with manager.session() as session:
            statuses = list_source_status(session)
        return [GraphQLSourceStatus(**item.model_dump()) for item in statuses]


schema = strawberry.Schema(query=Query)
