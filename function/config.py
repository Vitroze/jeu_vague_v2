from .utils import request_option, request_string, request_number, request_bool

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

def create_character():
    setup = {}
    for option in setup_character:
        request = send_request(option.get("name"), option.get("type"), min_value=option.get("min"), default=option.get("default"))
        setup[option.get("key")] = request

    print(setup)

options = [
    {
        "name": "Création d'un personnage",
        "callback": create_character,
    },
    {
        "name": "Modification d'un personnage",
        "callback": None,
    },
    {
        "name": "Supprimer un personnage",
        "callback": None
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