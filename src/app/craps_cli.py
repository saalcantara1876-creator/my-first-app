"""Play craps in the terminal: uv run python -m app.craps_cli"""

from collections.abc import Callable

from app.craps import DONT_PASS, PASS_LINE, CrapsGame

HELP = """
How a round works
  1. Before the come-out roll, bet on the pass line or on don't pass.
  2. Come-out roll: 7 or 11 wins for the pass line. 2, 3 or 12 loses.
     Any other number becomes "the point".
  3. The shooter keeps rolling. The point again wins for the pass line.
     A 7 loses ("seven-out"). Nothing else matters to the line bets.
  Don't pass is the opposite bet, except a come-out 12 is a tie.
  Both bets pay 1 to 1: bet $10, win $10.

Commands
  pass 10   bet $10 on the pass line
  dont 10   bet $10 on don't pass
  roll      roll the dice (or just press Enter)
  help      show this again
  quit      leave the table
"""

BET_COMMANDS = {"pass": PASS_LINE, "p": PASS_LINE, "dont": DONT_PASS, "d": DONT_PASS}


def describe_table(game: CrapsGame) -> str:
    """One line showing the phase, the bets on the table and the bankroll."""
    phase = "Come-out roll" if game.is_come_out else f"Point is {game.point}"
    bets = ", ".join(f"${amount} on {name}" for name, amount in game.bets.items()) or "no bets"
    return f"[{phase}] Bankroll: ${game.bankroll} | On the table: {bets}"


def handle_bet(game: CrapsGame, words: list[str]) -> str:
    """Place a bet from a command like ["pass", "10"] and return a reply."""
    if len(words) != 2 or not words[1].isdigit():
        return f"Type an amount too, like: {words[0]} 10"
    name = BET_COMMANDS[words[0]]
    try:
        game.place_bet(name, int(words[1]))
    except ValueError as error:
        return str(error)
    return f"${words[1]} on {name}."


def play(
    game: CrapsGame | None = None,
    read: Callable[[str], str] = input,
    write: Callable[[str], None] = print,
) -> None:
    """Run the game loop until the player quits or runs out of money."""
    game = game or CrapsGame()
    write("Welcome to the craps table!")
    write(HELP)
    while True:
        if game.bankroll == 0 and not game.bets:
            write("You're out of chips. Thanks for playing!")
            return
        write(describe_table(game))
        try:
            words = read("> ").lower().split()
        except EOFError:
            words = ["quit"]
        command = words[0] if words else "roll"
        if command in ("quit", "q"):
            write(f"You leave the table with ${game.bankroll}.")
            return
        if command in ("help", "h"):
            write(HELP)
        elif command in BET_COMMANDS:
            write(handle_bet(game, words))
        elif command in ("roll", "r"):
            result = game.roll()
            write(f"Rolled {result.dice[0]} + {result.dice[1]} = {result.total}")
            for message in result.messages:
                write(f"  {message}")
        else:
            write("I didn't understand that. Type 'help' to see the commands.")


if __name__ == "__main__":
    play()
