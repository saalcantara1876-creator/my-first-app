"""Craps rules: the come-out roll, the point, and the two line bets.

A round of craps has two phases:

1. The come-out roll. 7 or 11 wins for the pass line, 2, 3 or 12 loses.
   Any other number (4, 5, 6, 8, 9, 10) becomes "the point".
2. The point phase. The shooter keeps rolling until they roll the point
   again (pass line wins) or a 7 (pass line loses, called a "seven-out").

The don't pass bet is the opposite of the pass line, except that a 12 on
the come-out roll is a tie.
"""

import random
from dataclasses import dataclass

from app.dice import roll_two_dice

PASS_LINE = "pass line"
DONT_PASS = "don't pass"
LINE_BETS = (PASS_LINE, DONT_PASS)

WIN = "win"
LOSE = "lose"
PUSH = "push"  # a tie: you get your bet back


@dataclass
class RollResult:
    """What happened on one roll, with an explanation for the player."""

    dice: tuple[int, int]
    total: int
    messages: list[str]


class CrapsGame:
    """One player at a craps table, with a bankroll and bets on the table."""

    def __init__(self, bankroll: int = 100, rng: random.Random | None = None):
        self.bankroll = bankroll
        self.point: int | None = None  # None means the next roll is a come-out roll
        self.bets: dict[str, int] = {}
        self.rng = rng

    @property
    def is_come_out(self) -> bool:
        return self.point is None

    def place_bet(self, name: str, amount: int) -> None:
        """Move chips from the bankroll onto a line bet."""
        if name not in LINE_BETS:
            raise ValueError(f"Unknown bet: {name}")
        if not self.is_come_out:
            raise ValueError("Line bets can only be made before the come-out roll.")
        if amount <= 0:
            raise ValueError("A bet must be at least $1.")
        if amount > self.bankroll:
            raise ValueError(f"You only have ${self.bankroll}.")
        self.bankroll -= amount
        self.bets[name] = self.bets.get(name, 0) + amount

    def roll(self, dice: tuple[int, int] | None = None) -> RollResult:
        """Roll the dice, settle the bets and return what happened.

        Pass dice like (3, 4) to force a specific roll.
        """
        dice = dice or roll_two_dice(self.rng)
        total = sum(dice)
        if self.is_come_out:
            outcomes, messages = self._come_out_roll(total)
        else:
            outcomes, messages = self._point_roll(total)
        messages += self._settle_bets(outcomes)
        return RollResult(dice, total, messages)

    def _come_out_roll(self, total: int) -> tuple[dict[str, str], list[str]]:
        if total in (7, 11):
            message = f"{total} on the come-out roll is a 'natural': the pass line wins."
            return {PASS_LINE: WIN, DONT_PASS: LOSE}, [message]
        if total in (2, 3):
            message = f"{total} on the come-out roll is 'craps': the pass line loses."
            return {PASS_LINE: LOSE, DONT_PASS: WIN}, [message]
        if total == 12:
            message = (
                "12 on the come-out roll is 'craps': the pass line loses. "
                "Don't pass ties on 12, which is how the casino keeps its edge."
            )
            return {PASS_LINE: LOSE, DONT_PASS: PUSH}, [message]
        self.point = total
        message = (
            f"The point is {total}. The shooter keeps rolling until they roll "
            f"{total} again (pass line wins) or a 7 (don't pass wins)."
        )
        return {}, [message]

    def _point_roll(self, total: int) -> tuple[dict[str, str], list[str]]:
        if total == self.point:
            self.point = None
            message = f"The shooter made the point ({total}): the pass line wins."
            return {PASS_LINE: WIN, DONT_PASS: LOSE}, [message]
        if total == 7:
            self.point = None
            message = "Seven-out: the pass line loses and don't pass wins."
            return {PASS_LINE: LOSE, DONT_PASS: WIN}, [message]
        message = (
            f"{total} doesn't settle the line bets. Still rolling for the point ({self.point})."
        )
        return {}, [message]

    def _settle_bets(self, outcomes: dict[str, str]) -> list[str]:
        """Pay out or collect each bet that was decided. Line bets pay 1 to 1."""
        messages = []
        for name, outcome in outcomes.items():
            amount = self.bets.pop(name, 0)
            if amount == 0:
                continue
            if outcome == WIN:
                self.bankroll += amount * 2  # your bet back plus the same again
                messages.append(f"Your {name} bet wins ${amount} (pays 1 to 1).")
            elif outcome == PUSH:
                self.bankroll += amount
                messages.append(f"Your {name} bet is a push: you get your ${amount} back.")
            else:
                messages.append(f"Your {name} bet loses ${amount}.")
        return messages
