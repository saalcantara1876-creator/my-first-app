"""Simulate rolling two six-sided dice."""

import random

SIDES = 6


def roll_die(rng: random.Random | None = None) -> int:
    """Roll one die and return a number from 1 to 6."""
    rng = rng or random
    return rng.randint(1, SIDES)


def roll_two_dice(rng: random.Random | None = None) -> tuple[int, int]:
    """Roll two dice and return both values, e.g. (3, 5).

    Pass a seeded random.Random to get repeatable rolls.
    """
    return roll_die(rng), roll_die(rng)


if __name__ == "__main__":
    first, second = roll_two_dice()
    print(f"You rolled {first} and {second} (total {first + second})")
