from ctpc.core.types import RankingProfile
from ctpc.services.ranking import rank_targets_for_disease


def test_rank_targets_for_ulcerative_colitis_returns_expected_order() -> None:
    scorecards = rank_targets_for_disease("MONDO:0005101", RankingProfile.BALANCED)

    ranked_targets = [scorecard.target_symbol for scorecard in scorecards]

    assert ranked_targets[:3] == ["IL23R", "JAK1", "TNF"]


def test_rank_targets_exposes_explanation_and_provenance() -> None:
    scorecard = rank_targets_for_disease("MONDO:0005101", RankingProfile.BALANCED)[0]

    assert scorecard.overall_score == 68.1
    assert scorecard.percentile == 99
    assert scorecard.explanation.summary.startswith("IL23R ranks highly")
    assert len(scorecard.explanation.supporting_evidence) >= 2
    assert scorecard.explanation.risk_evidence[0].source == "openfda"
