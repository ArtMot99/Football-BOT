import random


def divide_into_teams(players, team_size=5) -> list:
    """
    Разделяет список игроков на команды заданного размера.
    Если игроков недостаточно для полного формирования команд, оставшиеся идут в последнюю команду.
    """
    # Перетасовываем игроков случайным образом
    random.shuffle(players)
    teams = [players[i:i + team_size] for i in range(0, len(players), team_size)]
    return teams
