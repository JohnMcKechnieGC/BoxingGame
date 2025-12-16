"""
Fight simulation logic using only functions and dictionaries.
"""

from __future__ import annotations

import math
import random
from typing import Dict, List

SCORECARD_TEMPLATE = "Round {round_num}: {a_name} {a_score}-{b_score} {b_name}"


def build_state(fighter):
    """Create mutable state for a fighter."""
    stats = fighter["stats"]
    return {
        "stamina": stats["stamina"] * 10,
        "damage": 0,
        "rounds_won": 0,
        "score": 0,
    }


def effective_activity(stat_speed, stamina):
    """Adjust activity based on speed and current stamina."""
    stamina_factor = max(0.4, stamina / 80)
    return stat_speed * stamina_factor


def choose_strategy(style, round_num, total_rounds, score_margin):
    """
    Decide how risky a fighter should box this round.

    Returns a float where >1 is more aggressive, <1 is more cautious.
    """
    late_fight = round_num > total_rounds * 0.6
    behind = score_margin < 0

    if style == "pressure":
        base = 1.15
    elif style == "counter-puncher":
        base = 0.9
    elif style == "out-boxer":
        base = 0.85
    else:
        base = 1.0

    if late_fight and behind:
        base += 0.15
    elif late_fight and not behind:
        base -= 0.05
    return max(0.7, min(base, 1.35))


def punch_totals(attacker, defender, strategy, rng):
    """Estimate punches thrown and landed in a round."""
    activity = effective_activity(attacker["stats"]["speed"], attacker["state"]["stamina"])
    base_thrown = rng.randint(30, 55)
    thrown = int(base_thrown * (0.8 + activity / 12) * strategy)
    thrown = max(20, min(thrown, 90))

    accuracy = attacker["stats"]["speed"] * 0.9 + (10 - defender["stats"]["defense"]) * 0.5
    accuracy += (attacker["state"]["stamina"] - defender["state"]["stamina"]) * 0.03
    accuracy = max(18, min(accuracy, 60))
    landed = int(thrown * accuracy / 100)
    landed = max(5, min(landed, thrown))
    return thrown, landed


def body_work_bonus(attacker):
    """Give pressure and boxer-punchers a small perk to sap stamina."""
    style = attacker["style"]
    if style in {"pressure", "boxer-puncher"}:
        return 0.6
    if style == "counter-puncher":
        return 0.2
    return 0.4


def apply_damage(attacker, defender, landed, rng):
    """Apply damage, stun, and knockdown chances."""
    power = attacker["stats"]["power"]
    chin = defender["stats"]["chin"]
    heart = defender["stats"]["heart"]

    damage = landed * (power * 0.35)
    damage *= rng.uniform(0.7, 1.1)
    defender["state"]["damage"] += damage / 20

    # fatigue comes from both throw rate and absorbed punishment
    stamina_tax = landed * 0.15 + body_work_bonus(attacker)
    defender["state"]["stamina"] = max(10, defender["state"]["stamina"] - stamina_tax)

    # knockdown check
    kd_chance = (power * 1.4 + landed * 0.25) - chin * 1.1
    kd_chance = max(0, kd_chance + rng.uniform(-3, 3))
    knocked_down = kd_chance > 12 and rng.random() < kd_chance / 100
    stunned = kd_chance > 8 and rng.random() < kd_chance / 80
    return knocked_down, stunned


def score_round(landed_a, landed_b, kd_a=False, kd_b=False):
    """
    Standard 10-point must with knockdown adjustments.

    A knockdown normally creates a 10-8 round unless the other boxer dominated.
    """
    if landed_a == landed_b:
        base_a, base_b = 10, 10
    elif landed_a > landed_b:
        base_a, base_b = 10, 9
    else:
        base_a, base_b = 9, 10

    if kd_a and kd_b:
        return base_a, base_b
    if kd_a:
        base_a -= 1
        base_b += 1
    if kd_b:
        base_b -= 1
        base_a += 1

    base_a = max(7, base_a)
    base_b = max(7, base_b)
    return base_a, base_b


def round_commentary(round_num, fighter_a, fighter_b, landed_a, landed_b, kd_a, kd_b):
    """Create quick flavor text for the round."""
    leading = fighter_a["name"] if landed_a >= landed_b else fighter_b["name"]
    swing = "traded momentum" if abs(landed_a - landed_b) < 6 else f"{leading} dictated"
    kd_note = ""
    if kd_a and kd_b:
        kd_note = "both hit the deck!"
    elif kd_a:
        kd_note = f"{fighter_a['name']} dropped {fighter_b['name']}!"
    elif kd_b:
        kd_note = f"{fighter_b['name']} dropped {fighter_a['name']}!"
    return f"Round {round_num}: {swing}. {kd_note}".strip()


def format_scorecard(score_history, fighter_a, fighter_b):
    """Pretty-print round-by-round scores."""
    lines = []
    for entry in score_history:
        lines.append(
            SCORECARD_TEMPLATE.format(
                round_num=entry["round"],
                a_name=fighter_a["name"],
                b_name=fighter_b["name"],
                a_score=entry["a_score"],
                b_score=entry["b_score"],
            )
        )
    return "\n".join(lines)


def simulate_round(round_num, fighter_a, fighter_b, rng):
    """Simulate a single round and return scoring plus notes."""
    score_margin = fighter_a["state"]["score"] - fighter_b["state"]["score"]
    strategy_a = choose_strategy(fighter_a["style"], round_num, fighter_a["total_rounds"], score_margin)
    strategy_b = choose_strategy(fighter_b["style"], round_num, fighter_b["total_rounds"], -score_margin)

    thrown_a, landed_a = punch_totals(fighter_a, fighter_b, strategy_a, rng)
    thrown_b, landed_b = punch_totals(fighter_b, fighter_a, strategy_b, rng)

    kd_b, stunned_b = apply_damage(fighter_a, fighter_b, landed_a, rng)
    kd_a, stunned_a = apply_damage(fighter_b, fighter_a, landed_b, rng)

    # stunned fighters lose a bit of offense mid-round
    if stunned_a:
        landed_a = int(landed_a * 0.9)
    if stunned_b:
        landed_b = int(landed_b * 0.9)

    score_a, score_b = score_round(landed_a, landed_b, kd_a, kd_b)
    fighter_a["state"]["score"] += score_a
    fighter_b["state"]["score"] += score_b
    if score_a > score_b:
        fighter_a["state"]["rounds_won"] += 1
    elif score_b > score_a:
        fighter_b["state"]["rounds_won"] += 1

    commentary = round_commentary(round_num, fighter_a, fighter_b, landed_a, landed_b, kd_a, kd_b)
    return {
        "round": round_num,
        "thrown_a": thrown_a,
        "landed_a": landed_a,
        "thrown_b": thrown_b,
        "landed_b": landed_b,
        "a_score": score_a,
        "b_score": score_b,
        "kd_a": kd_a,
        "kd_b": kd_b,
        "commentary": commentary,
    }


def declare_winner(fighter_a, fighter_b):
    """Return a human-readable verdict."""
    total_a = fighter_a["state"]["score"]
    total_b = fighter_b["state"]["score"]
    if total_a == total_b:
        return "Draw"
    winner = fighter_a if total_a > total_b else fighter_b
    loser = fighter_b if winner is fighter_a else fighter_a

    margin = abs(total_a - total_b)
    verdict = "unanimous decision" if margin > 6 else "split-decision style win"
    return f"{winner['name']} wins by {verdict} over {loser['name']}."


def simulate_fight(fighter_a: Dict, fighter_b: Dict, *, rounds=10, seed=None, verbose=False) -> Dict:
    """
    Run a full fight and return a summary dictionary.
    """
    rng = random.Random(seed)
    fighter_a = dict(fighter_a)
    fighter_b = dict(fighter_b)
    fighter_a["state"] = build_state(fighter_a)
    fighter_b["state"] = build_state(fighter_b)
    fighter_a["total_rounds"] = rounds
    fighter_b["total_rounds"] = rounds

    history: List[Dict] = []
    commentary_lines: List[str] = []

    for r in range(1, rounds + 1):
        round_result = simulate_round(r, fighter_a, fighter_b, rng)
        history.append(round_result)
        commentary_lines.append(round_result["commentary"])
        if verbose:
            print(round_result["commentary"])

    verdict = declare_winner(fighter_a, fighter_b)
    scorecard = format_scorecard(history, fighter_a, fighter_b)
    return {
        "fighter_a": fighter_a,
        "fighter_b": fighter_b,
        "rounds": history,
        "scorecard": scorecard,
        "verdict": verdict,
        "commentary": commentary_lines,
    }
