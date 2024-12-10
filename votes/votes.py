import json
from pathlib import Path


VOTES_FILE = Path("votes.json")


def load_votes() -> set:
    """
    Loads the votes file, if there is no file -> returns and empty set.
    """
    if VOTES_FILE.exists():
        with open(VOTES_FILE, "r") as file:
            return set(json.load(file))

    return set()


def save_votes(votes: set) -> None:
    """
    Writes data from the survey to a file.
    """
    with open(VOTES_FILE, "w") as file:
        json.dump(list(votes), file)


def clear_votes() -> None:
    """
    Delete the file if it exists and ignore the error if file does not exist.
    """
    VOTES_FILE.unlink(missing_ok=True)


VOTES = load_votes()
