from function.score import sorted_score, print_score
from models.vague import Vague

class Game:
    def __init__(self, player, vague: Vague):
        self.player = player
        self.vague = vague

    def save_game(self):
        pass

    def load_game(self):
        pass

    def launch_game(self):
        pass

    def show_leaderboard(self):
        scores = sorted_score()
        print_score(scores)

    def exit(self):
        pass