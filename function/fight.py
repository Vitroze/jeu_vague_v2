from .generator import generate_character
from .utils import clear
from test_file import example_character
from time import sleep
from random import choice

def is_allies_alives(team):
    return any(allies.is_alive() for allies in team)

def random_list(team):
    return choice(team)

def select_character_if_death(character, callback, array)->bool:
    if character.is_death():
        return callback(array)

    return character

def take_damage_monster(team, monster, all_monsters):
    for allies in team:
        monster.take_damage(allies)

    return select_character_if_death(monster, generate_character, all_monsters)

def take_damage_allies(allies_choose, team, monster):
    allies_choose.take_damage(monster)

    if not is_allies_alives(team):
        return False

    return select_character_if_death(allies_choose, random_list, [allies for allies in team if allies.is_alive()])

def start_fight(team):
    all_monsters = [monster for monster in example_character if monster.get("is_ennemy")]
    monster = generate_character(all_monsters)
    allies_choose = random_list(team)

    return all_monsters, monster, allies_choose

def show_score(score, fight_in_progress: bool = False):
    if fight_in_progress:
        print(f"Phase {score} passé !")
    else:
        print(f"Vous avez survécu : {score} tours")

    sleep(1.25)

def fight(username, team):
    all_monsters, monster, allies_choose = start_fight(team)

    score = 0
    while is_allies_alives(team):
        clear()

        monster = take_damage_monster(team, monster, all_monsters)
        allies_choose = take_damage_allies(allies_choose, team, monster)
        if allies_choose == False:
            break

        score += 1
        show_score(score, True)

    show_score(score)