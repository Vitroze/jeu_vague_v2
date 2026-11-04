from .utils import clear, request_option, request_string
from .fight import fight
from meta.character import Character
from database.function import get_allies_in_db
MAX_TEAM = 2

def can_add_in_team(allies, name_team):
    return not allies.get("is_ennemy") and allies.get("name") not in name_team

def generate_list_team(team):
    name_team = [ available_character.name for available_character in team ]
    available_character = [
        available_character for available_character in get_allies_in_db()
        if can_add_in_team(available_character, name_team)
    ]

    return available_character

def create_team():
    team = []

    while len(team) < MAX_TEAM:
        clear()

        available_characters = generate_list_team(team)
        id_character = request_option(available_characters)
        character = Character.create_character(available_characters[id_character])

        team.append(character)

    return team

def play():
    username = request_string("Quel est votre nom d'utilisateur ?")
    team = create_team()

    fight(username, team)