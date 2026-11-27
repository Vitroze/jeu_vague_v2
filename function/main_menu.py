from function.game import play, resume
from function.config import menu_config
from function.utils import request_option_affichage, clear
from function.score import show_score
from models.vue import VueEcranTitre

options = [
    {
        "name": "Configurer",
        "callback": menu_config,
    },
    {
        "name": "Jouer",
        "callback": play,
    },
    {
        "name": "Reprendre",
        "callback": resume,
    },
    {
        "name": "Score",
        "callback": show_score,
    }
]

def show_menu():
    clear()
    # vue = VueEcranTitre()
    # affichage.update_live(vue)

    # value = request_option(options)
    # options[value]["callback"]()

    value = request_option_affichage(options)
    options[value]["callback"]()