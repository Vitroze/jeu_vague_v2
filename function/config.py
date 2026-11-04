from .utils import request_option, request_string, request_number, request_bool
from database.function import save_character, get_characters, delete_character as delete_character_db

def send_request(question, type, min_value=None, default=None):
    match (type):
        case "str":
            return request_string(question, default=default)
        case "int":
            return request_number(question, min=min_value, default=default)
        case "uint":
            return request_number(question, min=min_value is None and 0 or min_value, default=default)
        case "bool":
            return request_bool(question, default)

setup_character = [
    {
        "name": "Son nom ?",
        "type": "str",
        "key": "name"
    },
    {
        "name": "Sa vie ?",
        "type": "uint",
        "min": 1,
        "key": "health"
    },
    {
        "name": "Sa puissance d'attaque ?",
        "type": "uint",
        "key": "power_attack"
    },
    {
        "name": "Sa puissance de défense ?",
        "type": "uint",
        "key": "power_defense",
    },
    {
        "name": "Es-ce un ennemi ?",
        "type": "bool",
        "key": "is_ennemy",
        "default": False,
    }
]

def request_option_character()->dict:
    id_character = request_option(get_characters())
    try:
        character = get_characters()[id_character]
    except Exception:
        print("Le personnage n'existe pas !")
        return

    return character

def send_setup(character=None):
    setup = {}
    for option in setup_character:
        request = send_request(option.get("name"), option.get("type"), min_value=option.get("min"), default=character is not None and character[option.get("key")] or option.get("default"))
        setup[option.get("key")] = request
    return setup

def create_character():
    setup = send_setup()
    save_character(setup)

def update_character():
    character = request_option_character()

    setup = send_setup(character)
    save_character(setup, character.get("_id"))

def delete_character():
    character = request_option_character()
    confirm = request_bool("Êtes-vous sûre de supprimer le personnage ?")
    if confirm:
        delete_character_db(character.get("_id"))

options = [
    {
        "name": "Création d'un personnage",
        "callback": create_character,
    },
    {
        "name": "Modification d'un personnage",
        "callback": update_character,
    },
    {
        "name": "Supprimer un personnage",
        "callback": delete_character,
    },
    # TODO: Make a config items
    {
        "name": "Supprimer un score",
        "callback": None
    }
]

def menu_config():
    value = request_option(options)
    options[value]["callback"]()