from meta.character import Character
from function.utils import is_valid_list
from random import choice

def random_list(team):
    return choice(team)

def generate_character(list_character) -> Character|None:
    if not is_valid_list(list_character):
        return None

    choose_monster = random_list(list_character)
    choose_monster = Character.create_character(choose_monster)

    return choose_monster