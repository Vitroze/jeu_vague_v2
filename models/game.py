from function.score import sorted_score, print_score
from models.database import CharacterSaveDB, MonsterSaveDB
from models.vague import Vague
from database.function import save_game as save_game_db

class Game:
    _instance = None  # Variable de classe pour stocker l'instance unique

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self, player=None, vague: Vague = None):
        if not hasattr(self, 'initialized'):  # Vérifie si l'instance a déjà été initialisée
            self.initialized = True
            self.player = player
            self.vague = vague

    def save_game(self):
        """
        player_name,
        score,
        equipe (in charactersavedb)
        monsters (in monstersavedb)
        inventaire (in itemsavedb)
        """

        print(self.player, self.player.name, self.player.score, self.player.characters, self.vague.ennemies, self.player.inventory)

        save_game_db(
            player_name=self.player.name,
            score=self.player.score,
            team=[CharacterSaveDB(name=character.name, health=character.health, equipement=character.equipments) for character in self.player.characters],
            ennemies=[MonsterSaveDB(name=monster.name, health=monster.health) for monster in self.vague.ennemies],
            items=self.player.inventory,
        )

    def load_game(self):
        pass

    def launch_game(self):
        pass

    def show_leaderboard(self):
        scores = sorted_score()
        print_score(scores)

    def exit(self):
        pass

    @classmethod
    def get_current_game(cls):
        return cls._instance