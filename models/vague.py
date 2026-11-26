from .character import Enemy
from .item import Item
from .player import Player
from typing import List, Dict

class Vague:
    def __init__(self, vague: int = 1):
        self.vague = vague
        self.player = Player | None = None
        self.ennemies = List[Enemy] = []
        self.waves = List[dict] = []
        self.difficulties = List[dict] = []
        self.items = Dict[str, Item] = {}

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

    def pick_ennemies(self) -> List[Enemy]:
        number = (self.vague - 1) % 30 + 1
        wave = next(w for w in self._waves if w["start_number"] <= number <= w["end_number"])
        level = self.get_difficulty()
        difficulty = next(d for d in self._difficulties if d["lap"] == level)

        self.ennemies = [
            self.create_enemy(ennemy_info, difficulty)
            for ennemy_info in wave["monsters"]
        ]

    def pick_items(self) -> List[Item]:
        level = self.get_difficulty()
        difficulty = next(d for d in self._difficulties if d["lap"] == level)
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

    def play_vague(self):
        player, screen = self._player, None # TODO: Implement screen
        if not self.ennemies:
            self.pick_enemies()

        while self.ennemies and player.is_team_alive():
            for character in [target for target in player.team if target.is_alive()]:
                if not self.ennemies:
                    break

                # action = screen.DisplayVue(
                #     lambda: vue.VueTourJoueur(player.team, character, self.ennemies))
                # if action == "inventaire":
                #     player.CheckInventory()

                character._targets, character._targets_team = self.ennemies, player.team
                character.play_turn()
                for dead in self.get_ennemies_death():
                    self.death_ennemy(dead)

            for monster in self.ennemies:
                monster._targets = player.team
                monster.play_turn()

            # screen.DisplayVue(
            #     lambda: vue.VueInfoTour(player.team, "Fin du tour", self.ennemies))

        if player.is_team_alive():
            self.add_score(1)