from meta.character import Character, create_character
from function.utils import is_valid_list
from random import choice

def generate_character(list_character) -> Character|None:
    if not is_valid_list(list_character):
        return None

    choose_monster = choice(list_character)
    choose_monster = create_character(choose_monster)

    return choose_monster

# print("Monster :", generater_character([monster for monster in example_character if monster.get("is_ennemy")]))
# print("Gentil :", generater_character([monster for monster in example_character if not monster.get("is_ennemy")]))