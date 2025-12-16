"""
Boxing game package.

The project intentionally avoids classes to keep the design friendly for
students who are still learning Python fundamentals. Everything is expressed
with functions and dictionaries so the program flow stays approachable.
"""

from .fighters import roster, select_fighter
from .fight import simulate_fight, format_scorecard
