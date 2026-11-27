from models.vue import VueSelectionEquipe

from .character import Character
from .item import Item, Consumable, Equipable
from typing import List
from function.utils import clear, request_option
from .affichage import Affichage

def can_add_in_team(allies, name_team):
    if isinstance(allies, Character):
        return allies.is_alive() and allies.name not in name_team

    return not allies.get("is_ennemy") and allies.get("name") not in name_team

def generate_list_team(team, all_characters: List[dict]):
    name_team = [ available_character.name for available_character in team ]
    available_character = [
        available_character for available_character in all_characters
        if can_add_in_team(available_character, name_team)
    ]

    return available_character

MAX_TEAM = 6
class Player:
    def __init__(self, name: str, score: int = 0, characters: List[Character] = [], inventory: List["Item"] = []):
        self.name = name
        self.score = score
        self.characters = characters
        self.inventory = inventory

    def pick_character(self):
        characters = [character for character in self.characters if character.is_alive()]
        if not characters:
            return None

        id_character = request_option(characters)
        character = characters[id_character]
        return character

    def create_team(self, all_characters: List[dict]):
        team = []

        while len(team) < MAX_TEAM:
            available_characters = generate_list_team(team, all_characters)
            id_character =Affichage.display_vue(VueSelectionEquipe(team, available_characters))
            character = Character.create_character(available_characters[id_character])
            if character is None:
                continue

            team.append(character)
#             clear()

#             available_characters = generate_list_team(team, all_characters)
#             id_character = request_option(available_characters)
# #            character = Character.create_character(available_characters[id_character])
#             team.append(available_characters[id_character])

        self.characters = team

    def get_team_alive(self):
        return [character for character in self.characters if character.is_alive()]

    def is_team_alive(self):
        return any(character.is_alive() for character in self.characters)

    def use_item(self, item: Item, character: Character):
        if item not in self.inventory:
            return False

        if isinstance(item, Consumable):
            item.use(character)
        elif not (isinstance(item, Equipable) and character.equip_item(item)):
            return False

        self.inventory.remove(item)

    def get_inventory(self):
        return self.inventory

    def add_item(self, item: Item):
        self.inventory.append(item)

    def add_items(self, items: List[Item]):
        self.inventory.extend(items)