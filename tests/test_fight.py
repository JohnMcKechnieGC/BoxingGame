import pytest

from boxing_game.fight import declare_winner, score_round, simulate_fight
from boxing_game.fighters import roster, select_fighter


def test_score_round_knockdowns():
    # Fighter A is knocked down
    assert score_round(30, 25, kd_a=True, kd_b=False) == (9, 10)
    # Fighter B is knocked down
    assert score_round(18, 32, kd_a=False, kd_b=True) == (10, 9)
    # double knockdown stays neutral
    assert score_round(20, 20, kd_a=True, kd_b=True) == (10, 10)


def test_simulation_is_reproducible_with_seed():
    fighters = roster()
    result_1 = simulate_fight(fighters[0], fighters[1], rounds=6, seed=123)
    result_2 = simulate_fight(fighters[0], fighters[1], rounds=6, seed=123)
    assert result_1["scorecard"] == result_2["scorecard"]
    assert result_1["verdict"] == result_2["verdict"]


def test_verdict_tracks_scores():
    khan = select_fighter(1)
    duarte = select_fighter(2)
    result = simulate_fight(khan, duarte, rounds=4, seed=5)
    verdict = declare_winner(result["fighter_a"], result["fighter_b"])
    assert result["verdict"] == verdict
    assert "wins" in verdict or verdict == "Draw"
