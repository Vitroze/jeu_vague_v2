from .connect import *
from function.utils import clear_text
import re

def ignore_case(search: str):
    search = clear_text(search)
    return re.compile(f"^{re.escape(search)}$", re.IGNORECASE)

@is_connected
def is_exist_character(name, ennemy:bool=None):
    return get_collection("config").find_one({
        "name": ignore_case(name),
        "is_ennemy": ennemy
    }) != None


def is_validate_data_character(fc):
    def callback(*args, **kwars):
        if len(args) < 1 or type(args[0]) != dict:
            print("Merci de donner les données du personnage !")
            return

        character = args[0]
        if (not character.get("name")
            or not character.get("health")
            or not character.get("power_attack")
            or not character.get("power_defense")
            or character.get("is_ennemy") is None):
            print("Les données du personnage ne sont pas valides !")
            return

        return fc(*args, **kwars)
    return callback

@is_connected
@is_validate_data_character
def update_character(setup: dict, id_object: int):
    get_collection("config").update_one({
        "_id": id_object,
    }, {
        "$set": setup
    })
    print(f"Vous avez mise à jour le personnage !")

@is_connected
@is_validate_data_character
def save_character(setup: dict, id_object: int = None):
    if id_object:
        update_character(setup, id_object)
        return

    if is_exist_character(setup.get("name")):
        print("Votre personnage existe déjà !")
        return

    get_collection("config").insert_one(setup)
    print(f"Vous avez crée le personnage : {setup.get("name")}")

@is_connected
def delete_character(id_object: int = None):
    if not id_object:
        print("Vous devez spécifié un id pour supprimer le personnage !")
        return

    get_collection("config").delete_one({
        "_id": id_object,
    })

    print("Votre personnage a été supprimer !")

@is_connected
def get_ennemies_in_db():
    return list(get_collection("config").find({
        "is_ennemy": True,
    }))

@is_connected
def get_allies_in_db():
    return list(get_collection("config").find({
        "is_ennemy": False
    }))

@is_connected
def get_characters():
    return list(get_collection("config").find())

@is_connected
def get_scores():
    return list(get_collection("playerdata").find())

@is_connected
def get_playerdata_username(username: str):
    return get_collection("playerdata").find_one({
        "player_name": ignore_case(username)
    })


@is_connected
def is_exist_username(username: str):
    return get_playerdata_username(username) != None

def is_best_score(score: int, best_score: int):
    return score > best_score

@is_connected
def update_score(username:str, score:int):
    player_data = get_playerdata_username(username)
    if not is_best_score(score, player_data.get("score")):
        print("Vous avez pas battu votre record !")
        return

    get_collection("playerdata").update_one({
        "_id": player_data.get("_id")
    }, {
        "score": score,
    })

@is_connected
def add_score(username: str, score: int):
    if is_exist_username(username):
        update_score(username, score)
        return

    get_collection("playerdata").insert_one({
        "player_name": username,
        "score": score,
    })

@is_connected
def delete_score(id_object: int):
    if not id_object:
        return

    get_collection("playerdata").delete_one({
        "_id": id_object
    })