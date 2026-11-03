from .generator import generate_character
from .utils import clear
from test_file import example_character
from time import sleep
from random import choice

def is_allies_alives(team):
    return any(allies.is_alive() for allies in team)

def random_list(team):
    return choice(team)

def fight(username, team):
    all_monsters = [monster for monster in example_character if monster.get("is_ennemy")]
    monster = generate_character(all_monsters)
    allies_choose = random_list(team)

    score = 0
    while is_allies_alives(team):
        clear()
        for allies in team:
            monster.take_damage(allies)

        if not monster.is_alive():
            monster = generate_character(all_monsters)
            continue

        allies_choose.take_damage(monster)
        if not allies_choose.is_alive() and is_allies_alives(team):
            allies_choose = random_list([allies for allies in team if allies.is_alive()])

        score += 1

        print(f"Phase {score} passé !")

        sleep(1.25)