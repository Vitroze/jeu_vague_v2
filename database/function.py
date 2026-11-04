from .connect import *
from function.utils import clear_text
import re

def is_exist_character(name, ennemy:bool=None):
    return get_collection("config").find_one({
        "name": re.compile(f"^{re.escape(name)}$", re.IGNORECASE),
        "is_ennemy": ennemy
    })


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

    if is_exist_character(clear_text(setup.get("name"))):
        print("Votre personnage existe déjà !")
        return

    get_collection("config").insert_one(setup)
    print(f"Vous avez crée le personnage : {setup.get("name")}")

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