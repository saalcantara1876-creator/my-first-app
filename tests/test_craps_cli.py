import random

from app.craps import PASS_LINE, CrapsGame
from app.craps_cli import describe_table, handle_bet, play


def run(commands: list[str], game: CrapsGame) -> str:
    """Play with scripted commands and return everything that was printed."""
    remaining = iter(commands)
    output = []

    def read(prompt: str) -> str:
        try:
            return next(remaining)
        except StopIteration:
            raise EOFError from None

    play(game, read=read, write=output.append)
    return "\n".join(output)


def test_bet_and_roll_then_quit():
    game = CrapsGame(bankroll=100, rng=random.Random(0))
    output = run(["pass 10", "roll", "quit"], game)
    assert "$10 on pass line." in output
    assert "Rolled " in output
    assert "You leave the table with" in output


def test_empty_input_rolls_the_dice():
    output = run([""], CrapsGame(rng=random.Random(0)))
    assert "Rolled " in output


def test_end_of_input_quits():
    output = run([], CrapsGame(bankroll=100))
    assert "You leave the table with $100." in output


def test_help_and_unknown_commands():
    output = run(["help", "dance"], CrapsGame())
    assert output.count("How a round works") == 2  # once at the start, once for help
    assert "I didn't understand that" in output


def test_game_ends_when_out_of_chips():
    game = CrapsGame(bankroll=10, rng=random.Random(0))
    output = run(["pass 10"] + ["roll", "pass 10"] * 200, game)
    assert "You're out of chips" in output
    assert game.bankroll == 0


def test_handle_bet_needs_an_amount():
    game = CrapsGame()
    assert "like: pass 10" in handle_bet(game, ["pass"])
    assert "like: pass 10" in handle_bet(game, ["pass", "ten"])
    assert game.bets == {}


def test_handle_bet_reports_rule_errors():
    game = CrapsGame(bankroll=5)
    assert handle_bet(game, ["pass", "10"]) == "You only have $5."


def test_describe_table_shows_phase_bets_and_bankroll():
    game = CrapsGame(bankroll=100)
    assert describe_table(game) == "[Come-out roll] Bankroll: $100 | On the table: no bets"
    game.place_bet(PASS_LINE, 10)
    game.roll((2, 2))
    assert describe_table(game) == "[Point is 4] Bankroll: $90 | On the table: $10 on pass line"
