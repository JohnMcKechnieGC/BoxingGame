# Boxing Game (functions-only edition)

This project is a console boxing simulation designed for Python learners who
haven't started object-oriented programming yet. Everything is written with
functions and dictionaries so the program flow is easy to follow while still
showing how to structure a multi-file project.

### Quick start

```bash
python -m boxing_game
```

Pick two fighters, choose the number of rounds, and watch the scorecards
unfold. The program prints the random seed so you can replay the matchup.

### Project layout

- `boxing_game/fighters.py` — roster data and helper functions for selecting a fighter.
- `boxing_game/fight.py` — scoring, stamina, and round-by-round simulation.
- `boxing_game/main.py` — small CLI that wires everything together.

### Running tests

```bash
pytest
```

### Ideas to extend

- Add more fighters with unique stats and bios.
- Tweak the scoring algorithm to emphasize defense or ring generalship.
- Add saved scorecards and rivalries by persisting results to a file.
