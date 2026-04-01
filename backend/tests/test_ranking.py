from ctpc.services.ranking import overall_score, percentiles_from_scores


def test_overall_score_bounds():
    s = overall_score(80, 70, 60, 50, 8, 20)
    assert 0 <= s <= 100


def test_percentiles_order():
    p = percentiles_from_scores([10.0, 20.0, 30.0])
    assert p[2] >= p[0]
