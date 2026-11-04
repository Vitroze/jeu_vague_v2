from function.game import play
from function.config import menu_config
from function.utils import request_option, clear
from function.score import show_score

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
        "name": "Score",
        "callback": show_score,
    }
]

def show_menu():
    clear()

    value = request_option(options)
    options[value]["callback"]()