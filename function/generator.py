from meta.character import Character
from function.utils import is_valid_list
from random import choice

def is_valid_values_for_character(dict_character: dict)->bool:
    return dict_character.get("name") and dict_character.get("health") and dict_character.get("power_attack") and dict_character.get("power_defense")

def generater_character(list_character) -> Character|None:
    if not is_valid_list(list_character):
        return None

    choose_monster = choice(list_character)
    if not is_valid_values_for_character(choose_monster):
        return None

    choose_monster = Character(
        choose_monster["name"],
        choose_monster["health"],
        choose_monster["power_attack"],
        choose_monster["power_defense"],
        True
    )

    return choose_monster

# print("Monster :", generater_character([monster for monster in example_character if monster.get("is_ennemy")]))
# print("Gentil :", generater_character([monster for monster in example_character if not monster.get("is_ennemy")]))