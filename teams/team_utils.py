import random


def divide_into_teams(players, team_size=5) -> list:
    """
    Splits the list of players into teams of the specified size.
    If there are not enough players to form complete teams, the remaining players go to the last team.
    """
    random.shuffle(players)
    teams = [players[i:i + team_size] for i in range(0, len(players), team_size)]
    return teams
