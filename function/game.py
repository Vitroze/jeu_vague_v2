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

def new_game(no_verify: bool = False) -> Game:
    username = request_string("Quel est votre nom d'utilisateur (back pour revenir au menu principale) ?")
    if not no_verify and not check_username(username):
        return new_game()

    if username.lower() == "back":
        from function.main_menu import show_menu
        show_menu()
        return

    return Game(Player(username), Vague(), select_character)

def play():
    if not new_game().launch_game():
        print("Erreur lors du lancement du jeu. Veuillez réessayer.")

def resume():
    game = new_game(True)
    if not game.load_game():
        print("Aucune partie sauvegardée trouvée pour cet utilisateur.")
        return resume()

    game.launch_game()