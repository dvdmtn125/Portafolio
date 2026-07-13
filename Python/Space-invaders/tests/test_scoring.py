from src.core.scoring import increase_score


def test_increase_score_adds_one_by_default():
    assert increase_score(3) == 4


def test_increase_score_adds_custom_points():
    assert increase_score(10, 5) == 15