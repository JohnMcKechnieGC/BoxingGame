"""
Command-line interface for the boxing game.

The interface is intentionally small: pick two fighters, choose number of
rounds, and watch the scores unfold. Everything is function-based so students
can explore without classes.
"""

from __future__ import annotations

import random

from .fighters import roster, select_fighter
from .fight import format_scorecard, simulate_fight


def display_roster(pool):
    print("Available fighters:")
    for idx, fighter in enumerate(pool):
        rec = fighter["record"]
        print(
            f"[{idx}] {fighter['name']} ({rec['wins']}-{rec['losses']}-{rec['draws']} {rec['kos']} KOs) "
            f"- {fighter['style']} - {fighter['bio']}"
        )


def choose_indices(pool):
    while True:
        try:
            pick_a = int(input("Select the first fighter (number): "))
            pick_b = int(input("Select the opponent (number): "))
            if pick_a == pick_b:
                print("Pick different fighters for a matchup.")
                continue
            return pick_a, pick_b
        except (ValueError, IndexError):
            print("Enter valid numbers from the list.")


def prompt_rounds():
    try:
        rounds = int(input("How many rounds? (default 10) ") or 10)
    except ValueError:
        rounds = 10
    return max(4, min(rounds, 12))


def run_game(seed=None):
    pool = roster()
    display_roster(pool)
    pick_a, pick_b = choose_indices(pool)
    rounds = prompt_rounds()
    if seed is None:
        seed = random.randint(1, 9999)
    print(f"\nRing walks complete. Seed for rematches: {seed}\n")

    fighter_a = select_fighter(pick_a)
    fighter_b = select_fighter(pick_b)
    result = simulate_fight(fighter_a, fighter_b, rounds=rounds, seed=seed, verbose=True)

    print("\nScorecard:")
    print(format_scorecard(result["rounds"], result["fighter_a"], result["fighter_b"]))
    print("\nFinal Verdict:")
    print(result["verdict"])


if __name__ == "__main__":
    run_game()
