from .generator import generate_character
from .utils import clear
from database.function import get_ennemies_in_db, add_score as add_score_db
from meta.character import Character
from time import sleep
from random import choice

def is_allies_alives(team):
    return any(allies.is_alive() for allies in team)

def get_allies_alives(team):
    return [allies for allies in team if allies.is_alive()]

def random_list(team):
    return choice(team)

def start_fight(team):
    all_monsters = get_ennemies_in_db()
    monster = generate_character(all_monsters)
    allies_choose = random_list(team)

    return all_monsters, monster, allies_choose

def take_damage(character_target, character):
    character_target.take_damage(character)

def take_damage_list(character_target, list_character:list):
    for character in list_character:
        if character_target.is_death():
            break

        character_target.take_damage(character)

def manage_death(character, character_available:list):
    if character.is_death():
        new_character = random_list(character_available)
        if isinstance(new_character, dict):
            new_character = Character.create_character(new_character)

        return new_character
    return character

def show_score(score, fight_in_progress: bool = False):
    if fight_in_progress:
        print(f"Phase {score} passé !")
    else:
        print(f"Vous avez survécu : {score} tours")

    sleep(1.25)

def add_score(score):
    score += 1
    show_score(score, True)

    return score

def fight_rounds(allies_choose, monster, team):
    score = 0
    while allies_choose.is_alive() and monster.is_alive():
        take_damage_list(monster, team)
        take_damage(allies_choose, monster)
        score = add_score(score)

    return score

def fight(username, team):
    all_monsters, monster, allies_choose = start_fight(team)

    score = 0
    while is_allies_alives(team):
        clear()

        allies_choose = manage_death(allies_choose, get_allies_alives(team))
        monster = manage_death(monster, all_monsters)

        score += fight_rounds(allies_choose, monster, team)

    show_score(score)
    add_score_db(username, score)