"""
Fighter roster utilities.

All fighters are described with dictionaries instead of classes. Each fighter
has:
- bio: general info for commentary
- stats: ratings from 1-10
- style: boxing philosophy to guide strategy choices

The structure keeps things readable for learners while still supporting a
surprisingly varied fight simulation.
"""

import copy


def roster():
    """Return a fresh list of fighters so callers can freely modify entries."""
    return [
        {
            "name": "Elena \"Lightning\" Ruiz",
            "bio": "Olympic-style southpaw with snapping counters.",
            "style": "counter-puncher",
            "stance": "southpaw",
            "record": {"wins": 17, "losses": 1, "draws": 0, "kos": 7},
            "stats": {
                "power": 7,
                "speed": 9,
                "defense": 9,
                "chin": 7,
                "stamina": 8,
                "heart": 8,
            },
        },
        {
            "name": "Tariq \"Steamroller\" Khan",
            "bio": "Pressure fighter who hunts the body until opponents wilt.",
            "style": "pressure",
            "stance": "orthodox",
            "record": {"wins": 24, "losses": 2, "draws": 1, "kos": 19},
            "stats": {
                "power": 9,
                "speed": 7,
                "defense": 6,
                "chin": 8,
                "stamina": 9,
                "heart": 9,
            },
        },
        {
            "name": "Marcos \"Professor\" Duarte",
            "bio": "Jab-heavy tactician who stacks up points from range.",
            "style": "out-boxer",
            "stance": "orthodox",
            "record": {"wins": 30, "losses": 5, "draws": 0, "kos": 12},
            "stats": {
                "power": 6,
                "speed": 8,
                "defense": 8,
                "chin": 7,
                "stamina": 9,
                "heart": 7,
            },
        },
        {
            "name": "Riley \"Switchblade\" Moore",
            "bio": "Switch-hitter who blends angles with sneaky uppercuts.",
            "style": "boxer-puncher",
            "stance": "switch",
            "record": {"wins": 14, "losses": 0, "draws": 0, "kos": 11},
            "stats": {
                "power": 8,
                "speed": 8,
                "defense": 7,
                "chin": 8,
                "stamina": 7,
                "heart": 8,
            },
        },
    ]


def select_fighter(index):
    """
    Grab a fighter from the roster by numeric index.

    A deep copy is returned so the simulation can track stamina and damage
    without mutating the original template.
    """
    pool = roster()
    if not 0 <= index < len(pool):
        raise IndexError("pick a valid fighter index")
    return copy.deepcopy(pool[index])
