from .utils import clear, request_option, show_option, request_string
from .fight import fight
from meta.character import create_character
from test_file import example_character

MAX_TEAM = 2

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
    username = request_string("Quel est votre nom d'utilisateur ?")
    team = create_team()

    fight(username, team)