from .utils import request_option, request_string, clear
from models.game import Game
from models.vague import Vague
from models.player import Player
from database.function import is_exist_username
from time import sleep

def select_character(characters) -> int:
    clear()
    options = [
        {"name": f"{character.get('name')} (PV: {character.get('health')})", "value": character.get("name")}
        for character in characters if not character.get("is_ennemy")
    ]

    return request_option(options)

def check_username(username: str) -> bool:
    if is_exist_username(username):
        print("Ce nom d'utilisateur existe déjà !")
        sleep(.75)
        return False
    return True

def new_game() -> Game:
    username = request_string("Quel est votre nom d'utilisateur ?")
    if not check_username(username):
        return new_game()

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