from models.affichage import Affichage

from .character import Entity, Enemy
from .item import Item
from .player import Player
from function.generator import random_list
from typing import List, Dict
from time import sleep

def format_entities(entities: List[dict]) -> str:
    return "\n".join(
        f"{e['name']} (PV: {e['health']}/{e['max_health']})"
        for e in entities if e["health"] > 0
    )

def show_event(evenements: List[dict], vague: object):
    affichage = Affichage()

    for evenement in evenements:
        vue = affichage.create_multiples_info_boxes(
            titre=f"Vague {vague.vague}",
            infos=[
                {"title": "Équipe du joueur", "content": format_entities(evenement["team"])},
                {"title": "Événements du tour", "content": evenement["message"]},
                {"title": "Ennemis", "content": format_entities(evenement["enemies"])},
            ]
        )
        affichage.update_live(vue)
        sleep(1.25)

class Vague:
    def __init__(self, vague: int = 1, player: Player | None = None, ennemies: List[Enemy] = [], waves: List[dict] = [], difficulties: List[dict] = [], items: Dict[str, Item] = {}):
        self.vague = vague
        self.player = player
        self.ennemies = ennemies
        self.waves = waves
        self.difficulties = difficulties
        self.items = items
        self.on_turn = None

    def get_difficulty(self) -> int:
        return min((self.vague - 1) // 30 + 1, len(self.difficulties))

    def create_enemy(self, ennemy_info: dict, difficulty: dict) -> Enemy:
        return Enemy(
            ennemy_info["name"],
            int(ennemy_info["health"] * difficulty["health_multiplier"]),
            int(ennemy_info["power_attack"] * difficulty["attack_multiplier"]),
            int(ennemy_info["power_defense"] * difficulty["defense_multiplier"]),
            [self.items[n] for n in ennemy_info.get("dropable", []) if n in self.items]
        )

    def get_difficulty_config(self) -> dict:
        lap = self.get_difficulty()
        default = {"lap": lap, "health_multiplier": 1, "attack_multiplier": 1, "defense_multiplier": 1, "item_multiplier": 1}
        return next((d for d in self.difficulties if d["lap"] == lap), default)

    def pick_enemies(self) -> List[Enemy]:
        number = (self.vague - 1) % 30 + 1
        wave = next((w for w in self.waves if w["start_number"] <= number <= w["end_number"]), None)
        if wave is None:
            self.ennemies = []
            return self.ennemies

        difficulty = self.get_difficulty_config()
        self.ennemies = [
            self.create_enemy(ennemy_info, difficulty)
            for ennemy_info in wave["monsters"]
        ]

        return self.ennemies

    def restore(self, vague:int, saved_ennemies: List[dict], ennemy_docs: List[dict]):
        self.vague = vague
        templates = {doc["name"]: doc for doc in ennemy_docs}
        difficulty = self.get_difficulty_config()

        self.ennemies = []
        for saved_ennemy in saved_ennemies:
            if saved_ennemy["name"] in templates:
                ennemy = self.create_enemy(templates[saved_ennemy["name"]], difficulty)
                ennemy.set_health(saved_ennemy["health"])
                self.ennemies.append(ennemy)

    def death_ennemy(self, ennemy: Enemy):
        if ennemy in self.ennemies:
            self.ennemies.remove(ennemy)

            if self.player:
                self.player.add_items(ennemy.drop_loot(multiplier=self.get_difficulty_config().get("item_multiplier", 1.0)))

    def get_ennemies_death(self) -> List[Enemy]:
        return [ennemy for ennemy in self.ennemies if not ennemy.is_alive()]

    def add_score(self, score: int):
        if self.player:
            self.player.score += score

        self.vague += 1

    def describe_attack(self, attacker: Entity, target: Entity, damage: int) -> str:
        if target.is_death():
            return f"{target.name} a été vaincu par {attacker.name} !"

        return f"{attacker.name} inflige {damage} degats a {target.name}"

    def save_event(self, message: str) -> dict:
        return {
            "message": message,
            "team": [Character.to_dict() for Character in self.player.characters],
            "enemies": [Enemy.to_dict() for Enemy in self.ennemies],
        }

    def play_vague_round(self, allies_choose, monster_choose):
        monster_choose.target = allies_choose

        while allies_choose.is_alive() and monster_choose.is_alive():
            list_event = []

            for character in self.player.get_team_alive():
                if not monster_choose.is_alive():
                    break

                character.target = monster_choose
                damage = character.play_turn()
                if damage:
                    list_event.append(self.save_event(self.describe_attack(character, monster_choose, damage)))

            if monster_choose.is_alive():
                damage = monster_choose.play_turn()
                if damage:
                    list_event.append(self.save_event(self.describe_attack(monster_choose, allies_choose, damage)))

            show_event(list_event, self)

        return allies_choose.is_alive()

    def play_vague(self):
        player, screen = self.player, None # TODO: Implement screen
        if not player:
            return False

        if not self.ennemies:
            self.pick_enemies()

        if not self.ennemies:
            return False

        while self.ennemies and player.is_team_alive():
            allies_choose = random_list(player.characters)
            monster_choose = random_list(self.ennemies)

            self.play_vague_round(allies_choose, monster_choose)
            if not monster_choose.is_alive():
                self.death_ennemy(monster_choose)

        if player.is_team_alive():
            self.add_score(1)
            print(f"Vous avez survécu à la vague {self.vague - 1} !")

        sleep(.75)