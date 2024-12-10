import json
from pathlib import Path


VOTES_FILE = Path("votes.json")


def load_votes() -> set:
    if VOTES_FILE.exists():
        with open(VOTES_FILE, "r") as file:
            return set(json.load(file))

    return set()


def save_votes(votes: set) -> None:
    with open(VOTES_FILE, "w") as file:
        json.dump(list(votes), file)


def clear_votes() -> None:
    VOTES_FILE.unlink(missing_ok=True)


VOTES = load_votes()
