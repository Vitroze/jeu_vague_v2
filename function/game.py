from models import character
from .utils import request_option, request_string, clear
from models.game import Game
from models.vague import Vague
from models.player import Player
from models.affichage import Affichage
from database.function import get_allies_in_db, get_waves, get_difficulties

def select_character(characters) -> int:
    clear()
    options = [
        {"name": f"{character.get('name')} (PV: {character.get('health')})", "value": character.get("name")}
        for character in characters if not character.get("is_ennemy")
    ]

    return request_option(options)

def new_game() -> Game:
    username = request_string("Quel est votre nom d'utilisateur ?")
    return Game(Player(username), Vague(), select_character)

def play():
    if not new_game().launch_game():
        print("Erreur lors du lancement du jeu. Veuillez réessayer.")

def resume():
    game = new_game()
    if not game.load_game():
        print("Aucune partie sauvegardée trouvée pour cet utilisateur.")
        return

    game.launch_game()