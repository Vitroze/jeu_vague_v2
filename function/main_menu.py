from function.game import play
from function.config import menu_config
from function.utils import request_option, clear

def fake_call():
    """Fonction pour le test"""
    pass

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
        "callback": fake_call,
    }
]

def show_menu():
    clear()

    value = request_option(options)
    options[value]["callback"]()