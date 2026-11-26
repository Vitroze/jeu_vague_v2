from .character import Enemy
from .item import Item
from .player import Player
from function.generator import random_list
from typing import List, Dict
from time import sleep

class Vague:
    def __init__(self, vague: int = 1, player: Player | None = None, ennemies: List[Enemy] = [], waves: List[dict] = [], difficulties: List[dict] = [], items: Dict[str, Item] = {}):
        self.vague = vague
        self.player = player
        self.ennemies = ennemies
        self.waves = waves
        self.difficulties = difficulties
        self.items = items

    def get_difficulty(self) -> int:
        return min((self.vague - 1) // 30, len(self.difficulties) - 1)

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

    def pick_items(self) -> List[Item]:
        level = self.get_difficulty()
        difficulty = next(d for d in self.difficulties if d["lap"] == level)
        self.items = [
            self.items[n]
            for n in difficulty.get("items", [])
            if n in self.items
        ]

        return self.items

    def death_ennemy(self, ennemy: Enemy):
        if ennemy in self.ennemies:
            self.ennemies.remove(ennemy)
            self.player.add_items(ennemy.drop_loot())

    def get_ennemies_death(self) -> List[Enemy]:
        return [ennemy for ennemy in self.ennemies if not ennemy.is_alive()]

    def add_score(self, score: int):
        if self.player:
            self.player.score += score

        self.vague += 1

    def random_character(self, list_characters: List[dict]) -> dict:
        return random_list(list_characters, 1)[0]

    def play_vague_round(self, allies_choose, monster_choose):
        monster_choose.target = allies_choose
        while allies_choose.is_alive() and monster_choose.is_alive():
            for character in self.player.get_team_alive():
                if not monster_choose.is_alive():
                    break

                character.target = monster_choose
                character.play_turn()

            if not monster_choose.is_alive():
                break

            monster_choose.play_turn()

        return allies_choose.is_alive()

    def play_vague(self):
        player, screen = self.player, None # TODO: Implement screen
        if not self.ennemies:
            self.pick_enemies()

        print(f"Vague {self.vague} : {len(self.ennemies)} ennemis à affronter !")
        while self.ennemies and player.is_team_alive():
            allies_choose = random_list(player.characters)
            monster_choose = random_list(self.ennemies)

            print("=====================================")
            is_win = self.play_vague_round(allies_choose, monster_choose)
            if not monster_choose.is_alive():
                self.death_ennemy(monster_choose)
                print(f"{monster_choose.name} est mort !")
            print("=====================================")

            # for character in [target for target in player.characters if target.is_alive()]:
            #     if not self.ennemies:
            #         break

            #     # action = screen.DisplayVue(
            #     #     lambda: vue.VueTourJoueur(player.characters, character, self.ennemies))
            #     # if action == "inventaire":
            #     #     player.CheckInventory()

            #     character.targets, character.targets_team = self.ennemies, player.characters
            #     character.play_turn()
            #     for dead in self.get_ennemies_death():
            #         self.death_ennemy(dead)

            # for monster in self.ennemies:
            #     monster.targets = player.characters
            #     monster.play_turn()

            # screen.DisplayVue(
            #     lambda: vue.VueInfoTour(player.characters, "Fin du tour", self.ennemies))

        if player.is_team_alive():
            self.add_score(1)
            print(f"Vous avez survécu à la vague {self.vague - 1} !")

        sleep(.75)

    def start_vague(self):
        while self.player.is_team_alive():
            self.play_vague()
            if not self.player.is_team_alive():
                print(f"Vous avez perdu à la vague {self.vague} !")
                break