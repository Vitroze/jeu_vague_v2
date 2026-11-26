from .utils import request_string
from models.game import Game
from models.vague import Vague
from models.player import Player
from models.affichage import Affichage
from database.function import get_allies_in_db, get_waves, get_difficulties

def play():
    username = request_string("Quel est votre nom d'utilisateur ?")
    player = Player(username)
    player.create_team(get_allies_in_db())

    #fight(username, player.characters)

    vague = Vague(player=player, ennemies=[], waves=get_waves(), difficulties=get_difficulties(), items={})
    Game(player, vague)
    Affichage()

    vague.start_vague()