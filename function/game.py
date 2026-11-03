from .utils import clear, request_option, show_option
from meta.character import create_character

MAX_TEAM = 2

example_character = [
    {
        "name": "Antagoniste",
        "health": 100,
        "power_attack": 20,
        "power_defense": 10,
        "is_ennemy": True,
    },
    {
        "name": "Vrai gentil",
        "health": 92,
        "power_attack": 30,
        "power_defense": 4,
    },
    {
        "name": "gentil",
        "health": 92,
        "power_attack": 30,
        "power_defense": 4,
    }
]

def create_team():
    team = []

    while len(team) < MAX_TEAM:
        clear()

        name_team = [ allies.name for allies in team ]
        allies = [
            allies for allies in example_character if not allies.get("is_ennemy") and not allies.get("name") in name_team
        ]

        show_option(allies)
        id_character = request_option(allies)
        character = create_character(allies[id_character])
        if character is None:
            continue

        team.append(character)

    return team

def play():
    team = create_team()

    print(team)