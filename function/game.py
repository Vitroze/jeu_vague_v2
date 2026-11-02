from .utils import clear, request_option, show_option

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

        allies = [allies for allies in example_character if not allies.get("is_ennemy") and not allies.get("name") in team]

        show_option(allies)
        id_character = request_option(allies)
        team.append(allies[id_character].get("name"))


def play():
    team = create_team()