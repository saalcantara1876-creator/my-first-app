import random

import pytest

from app.craps import DONT_PASS, PASS_LINE, CrapsGame


def game_with_bets(pass_line: int = 0, dont_pass: int = 0) -> CrapsGame:
    game = CrapsGame(bankroll=100)
    if pass_line:
        game.place_bet(PASS_LINE, pass_line)
    if dont_pass:
        game.place_bet(DONT_PASS, dont_pass)
    return game


def test_placing_a_bet_moves_chips_to_the_table():
    game = game_with_bets(pass_line=10)
    assert game.bankroll == 90
    assert game.bets == {PASS_LINE: 10}


@pytest.mark.parametrize("dice", [(3, 4), (5, 6)])
def test_come_out_natural_wins_pass_line(dice):
    game = game_with_bets(pass_line=10)
    game.roll(dice)
    assert game.bankroll == 110
    assert game.bets == {}
    assert game.is_come_out


@pytest.mark.parametrize("dice", [(1, 1), (1, 2), (6, 6)])
def test_come_out_craps_loses_pass_line(dice):
    game = game_with_bets(pass_line=10)
    game.roll(dice)
    assert game.bankroll == 90
    assert game.bets == {}


@pytest.mark.parametrize("dice", [(3, 4), (5, 6)])
def test_come_out_natural_loses_dont_pass(dice):
    game = game_with_bets(dont_pass=10)
    game.roll(dice)
    assert game.bankroll == 90


@pytest.mark.parametrize("dice", [(1, 1), (1, 2)])
def test_come_out_2_or_3_wins_dont_pass(dice):
    game = game_with_bets(dont_pass=10)
    game.roll(dice)
    assert game.bankroll == 110


def test_come_out_12_is_a_push_for_dont_pass():
    game = game_with_bets(dont_pass=10)
    game.roll((6, 6))
    assert game.bankroll == 100
    assert game.bets == {}


@pytest.mark.parametrize("total", [4, 5, 6, 8, 9, 10])
def test_other_come_out_numbers_set_the_point(total):
    game = game_with_bets(pass_line=10)
    game.roll((total - 2, 2) if total <= 8 else (total - 6, 6))
    assert game.point == total
    assert game.bets == {PASS_LINE: 10}
    assert game.bankroll == 90


def test_making_the_point_wins_pass_line_and_loses_dont_pass():
    game = game_with_bets(pass_line=10, dont_pass=5)
    game.roll((2, 2))
    game.roll((1, 3))
    assert game.bankroll == 105  # 85 left + 20 back from the pass line
    assert game.bets == {}
    assert game.is_come_out


def test_seven_out_loses_pass_line_and_wins_dont_pass():
    game = game_with_bets(pass_line=10, dont_pass=5)
    game.roll((2, 2))
    game.roll((3, 4))
    assert game.bankroll == 95  # 85 left + 10 back from don't pass
    assert game.bets == {}
    assert game.is_come_out


def test_other_rolls_during_the_point_change_nothing():
    game = game_with_bets(pass_line=10)
    game.roll((2, 2))
    game.roll((5, 6))  # 11 only matters on the come-out roll
    game.roll((1, 1))
    assert game.point == 4
    assert game.bets == {PASS_LINE: 10}
    assert game.bankroll == 90


def test_roll_explains_what_happened():
    game = game_with_bets(pass_line=10)
    result = game.roll((3, 4))
    assert result.dice == (3, 4)
    assert result.total == 7
    assert any("pass line bet wins $10" in message for message in result.messages)


def test_cannot_bet_more_than_the_bankroll():
    game = CrapsGame(bankroll=5)
    with pytest.raises(ValueError):
        game.place_bet(PASS_LINE, 10)


@pytest.mark.parametrize("amount", [0, -5])
def test_bet_must_be_positive(amount):
    with pytest.raises(ValueError):
        CrapsGame().place_bet(PASS_LINE, amount)


def test_cannot_place_an_unknown_bet():
    with pytest.raises(ValueError):
        CrapsGame().place_bet("hard eight", 10)


def test_cannot_place_a_line_bet_once_the_point_is_set():
    game = CrapsGame()
    game.roll((2, 2))
    with pytest.raises(ValueError):
        game.place_bet(PASS_LINE, 10)


def test_random_rolls_keep_the_money_consistent():
    game = CrapsGame(bankroll=1000, rng=random.Random(1))
    for _ in range(500):
        if game.is_come_out and game.bankroll >= 10:
            game.place_bet(PASS_LINE, 10)
        game.roll()
        assert game.bankroll >= 0
        assert game.point in (None, 4, 5, 6, 8, 9, 10)
