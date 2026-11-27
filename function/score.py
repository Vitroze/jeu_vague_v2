from database.function import get_scores
from models.affichage import Affichage
from models.vue import VueEcranTitre, VueLeaderboard
from models.exceptions import UserQuit

def sorted_score():
    scores = get_scores()
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    return scores

def print_score(scores):
    print("------ Score ------")

    for index, object in enumerate(scores):
        print(f"    {index}. {object.get("player_name")} - {object.get("score")}")

def show_score():
    # 	def display_vue(cls, vue: Callable, max_index=1):
    scores = sorted_score()
    Affichage.display_vue(VueLeaderboard(scores), max_index=1)