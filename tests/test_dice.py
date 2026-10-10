import random

from app.dice import roll_die, roll_two_dice


def test_roll_die_is_between_1_and_6():
    rng = random.Random(0)
    assert all(1 <= roll_die(rng) <= 6 for _ in range(1000))


def test_roll_die_can_produce_every_face():
    rng = random.Random(0)
    assert {roll_die(rng) for _ in range(1000)} == {1, 2, 3, 4, 5, 6}


def test_roll_two_dice_returns_two_valid_values():
    rng = random.Random(0)
    for _ in range(1000):
        first, second = roll_two_dice(rng)
        assert 1 <= first <= 6
        assert 1 <= second <= 6


def test_roll_two_dice_is_repeatable_with_same_seed():
    assert roll_two_dice(random.Random(42)) == roll_two_dice(random.Random(42))


def test_roll_two_dice_works_without_a_seed():
    first, second = roll_two_dice()
    assert 1 <= first <= 6
    assert 1 <= second <= 6
