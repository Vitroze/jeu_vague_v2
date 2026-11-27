from database.function import get_scores
from models.affichage import Affichage
from models.vue import VueLeaderboard

def sorted_score():
    scores = get_scores()
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    return scores

def show_score():
    from function.main_menu import show_menu
    scores = sorted_score()
    Affichage.display_vue(VueLeaderboard(scores), max_index=1)
    show_menu()