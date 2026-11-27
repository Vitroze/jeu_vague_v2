from .utils import request_option, request_string, request_number, request_bool, request_password, password_is_correct
from database.function import (
    save_character, get_characters, delete_character as delete_character_db,
    get_scores, delete_score as delete_score_db,
    save_item, get_items, delete_item as delete_item_db
)
from datetime import datetime, timezone, timedelta
import os
import jwt

TTL = 60 # Seconds
METHOD_TOKEN = "HS384"

# As a way to simulate an admin system, this approach is very easy to bypass because it operates on the client side rather than the server side.
def save_token(token):
    with open("token.txt", "w+") as file:
        file.write(str(token))

def generate_token():
    return jwt.encode({
        "unique_id": "Vitroze", # Remplacer par une valeur serveur et unique (non modifiable par le client)
        "exp": datetime.now(timezone.utc) + timedelta(seconds=TTL),
        "iat": datetime.now(timezone.utc)
    }, os.getenv("SECRET_KEY_PAYLOAD"), algorithm=METHOD_TOKEN)

def decode_jwt(token:str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY_PAYLOAD"), algorithms=METHOD_TOKEN)
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    return payload

def get_access_token():
    try:
        with open("token.txt", "r") as file:
            if decode_jwt(file.read()):
                save_token(generate_token()) # Regenerate the token to extend its validity
                return True
            return False
    except FileNotFoundError:
        return False

def is_admin(fc):
    def callback(*args, **kwars):
        if get_access_token():
            return fc(*args, **kwars)

        request_password("Veuillez rentrer le mot de passe de l'admin (Laissez vide pour retourner au menu principale)", os.getenv("ADMIN_PASSWORD"))

        save_token(generate_token())
        return fc(*args, **kwars)

    return callback

@is_admin
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

@is_admin
def request_option_character()->dict:
    id_character = request_option(get_characters())
    try:
        character = get_characters()[id_character]
    except Exception:
        print("Le personnage n'existe pas !")
        return {}

    return character

@is_admin
def send_setup(setup_question, default_value=None):
    setup = {}
    for option in setup_question:
        request = send_request(option.get("name"), option.get("type"), min_value=option.get("min"), default=default_value is not None and default_value[option.get("key")] or option.get("default"))
        setup[option.get("key")] = request
    return setup

@is_admin
def create_character():
    setup = send_setup(setup_character)
    save_character(setup)

@is_admin
def update_character():
    character = request_option_character()

    setup = send_setup(setup_character, character)
    save_character(setup, character.get("_id"))

@is_admin
def delete_character():
    character = request_option_character()
    confirm = request_bool("Êtes-vous sûre de supprimer le personnage ?")
    if confirm:
        delete_character_db(character.get("_id"))

@is_admin
def delete_score():
    id_score = request_option(get_scores(), "player_name")
    score = get_scores()[id_score]

    confirm = request_bool(f"Êtes-vous sûre de supprimer le score de {score.get("player_name")}?")
    if confirm:
        delete_score_db(score.get("_id"))

setup_item = [
    {
        "name": "Nom de l'item",
        "type": "str",
        "key": "name"
    },
    {
        "name": "Bonus d'attaque",
        "type": "uint",
        "key": "power_attack"
    },
    {
        "name": "Bonus de défense",
        "type": "uint",
        "key": "power_defense"
    },
    {
        "name": "Durabilité",
        "type": "uint",
        "key": "durability"
    }
]

@is_admin
def request_option_item()->dict:
    id_item = request_option(get_items())
    try:
        item = get_items()[id_item]
    except Exception:
        print("L'item n'existe pas !")
        return {}

    return item

@is_admin
def create_item():
    setup = send_setup(setup_item)
    save_item(setup)

@is_admin
def update_item():
    item = request_option_item()

    setup = send_setup(setup_item, item)
    save_item(setup, item.get("_id"))

@is_admin
def delete_item():
    item = request_option_item()
    confirm = request_bool("Êtes-vous sûre de supprimer l'item ?")
    if confirm:
        delete_item_db(item.get("_id"))

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
    {
        "name": "Création d'un item",
        "callback": create_item,
    },
    {
        "name": "Modification d'un item",
        "callback": update_item,
    },
    {
        "name": "Supprimer un item",
        "callback": delete_item,
    },
    # TODO: Make a config items
    {
        "name": "Supprimer un score",
        "callback": delete_score
    }
]

@is_admin
def menu_config():
    value = request_option(options)
    options[value]["callback"]()