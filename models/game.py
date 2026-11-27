from time import sleep

from function.score import sorted_score, print_score
from models.affichage import Affichage
from database.function import (
    get_allies_in_db, get_ennemies_in_db, get_items, get_rarities, get_waves, get_difficulties,
    add_score as add_score_db, save_game as save_game_db, get_save, delete_save
)
from models.database import CharacterSaveDB, MonsterSaveDB
from models.character import Character, Enemy, Entity
from models.player import Player
from models.vague import Vague
from models.item import Item
from database.function import get_items, get_rarities, save_game as save_game_db

class Game:
    _instance = None  # Variable de classe pour stocker l'instance unique

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, player=None, vague: Vague = None, select=None):
        if not hasattr(self, 'initialized'):  # Vérifie si l'instance a déjà été initialisée
            self.initialized = True
            self.player = player
            self.vague = vague
            self.select = select
            self.affichage = Affichage()

        self.player = player or self.player
        self.vague = vague or self.vague
        self.select = select or self.select

    def load_config(self):
        rarities = get_rarities() or {}
        items = (Item.from_dict(item, rarities) for item in get_items())

        self.vague.waves = get_waves() or []
        self.vague.difficulties = get_difficulties() or []
        self.vague.items = {item.name: item for item in items if item is not None}

    def load_allies(self) -> list[Character]:
        allies = (Entity.create_character(ally) for ally in get_allies_in_db())
        return [ally for ally in allies if ally and not ally.is_ennemy]

    def save_game(self):
        if not self.player or not self.vague or not self.player.is_team_alive():
            return False

        save_game_db(
            player_name=self.player.name,
            score=self.player.score,
            team=[CharacterSaveDB(name=character.name, health=character.health, equipement=character.equipments) for character in self.player.characters],
            ennemies=[MonsterSaveDB(name=monster.name, health=monster.health) for monster in self.vague.ennemies],
            items=self.player.inventory,
            vague=self.vague.vague,
        )

        return True

    def load_game(self):
        data = get_save(self.player.name)
        if not data:
            return False

        self.load_config()
        allies = {info["name"]: info for info in get_allies_in_db()}

        team = []
        for saved in data.get("team", []):
            character = Entity.create_character(allies[saved["name"]]) if saved["name"] in allies else None
            if character is None:
                continue

            for name in saved.get("equipement", []):
                item = self.vague.items.get(name)
                if item and not item.consumable:
                    character.equip_item(item)
            character.set_health(saved.get("health", character.max_health))
            team.append(character)

        if not team:
            return False

        rarirties = get_rarities() or {}
        inventory = [
            self.vague.items.get(item["name"]) or Item.from_dict(item, rarirties)
            for item in data.get("items", [])
        ]

        self.player = Player(self.player.name, data.get("score", 0), team, [item for item in inventory if item is not None])
        self.vague.player = self.player
        self.vague.restore(data.get("vague", 1), data.get("ennemies", []), get_ennemies_in_db())
        return True

    def launch_game(self):
        self.load_config()

        if not self.player.characters:
            allies = self.load_allies()
            if not allies or not self.vague.waves:
                return False

            self.player.create_team(allies)

        self.vague.player = self.player

        while self.player.is_team_alive():
            if not self.vague.play_vague():
                break
            sleep(.75)

        if self.player.is_team_alive():
            return False

        print(f"Vous avez perdu à la vague {self.vague.vague} !")
        add_score_db(self.player.name, self.player.score)
        delete_save(self.player.name)
        return True

    def show_leaderboard(self):
        scores = sorted_score()
        print_score(scores)

    def exit(self):
        raise SystemExit("Exiting the game.")

    @classmethod
    def get_current_game(cls):
        return cls._instance