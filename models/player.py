from .character import Character
from .item import Item
from typing import List
from function.utils import clear, request_option
from function.game import generate_list_team

MAX_TEAM = 2
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

    def create_team(self):
        team = []

        while len(team) < MAX_TEAM:
            clear()

            available_characters = generate_list_team(team)
            id_character = request_option(available_characters)
            character = Character.create_character(available_characters[id_character])

            team.append(character)

        return team

    def is_team_alive(self):
        return any(character.is_alive() for character in self.characters)

    def use_item(self, item: Item, character: Character):
        if item.consumable:
            self.inventory.remove(item)

        if item.effect:
            item.use(character)

    def get_inventory(self):
        return self.inventory