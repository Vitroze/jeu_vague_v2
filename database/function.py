from .connect import is_connected, get_collection
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
        if len(args) < 1 or not isinstance(args[0], dict):
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
    print("Vous avez mise à jour le personnage !")

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
        "$set": { "score": score, }
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

@is_connected
def get_items():
    return list(get_collection("items").find())

def is_validate_data_item(fc):
    def callback(*args, **kwars):
        if len(args) < 1 or not isinstance(args[0], dict):
            print("Merci de donner les données de l'item !")
            return

        item = args[0]

        if ((not item.get("name") and item.get("name") == "")
            or (not item.get("power_attack") and item.get("power_attack") < 0)
            or (not item.get("power_defense") and item.get("power_defense") < 0)
            or (not item.get("durability") and item.get("durability") <= 0)):
            print("Les données de l'item ne sont pas valides !")
            return

        return fc(*args, **kwars)
    return callback

@is_connected
@is_validate_data_item
def save_item(setup: dict, id_object: int = None):
    if id_object:
        get_collection("items").update_one({
            "_id": id_object,
        }, {
            "$set": setup
        })
        print("Vous avez mise à jour l'item !")
        return

    get_collection("items").insert_one(setup)
    print(f"Vous avez crée l'item : {setup.get("name")}")

@is_connected
def delete_item(id_object: int = None):
    if not id_object:
        print("Vous devez spécifié un id pour supprimer l'item !")
        return

    get_collection("items").delete_one({
        "_id": id_object,
    })

    print("Votre item a été supprimer !")

# A temporary code that, in the event of a database reset, restores the default data for testing purposes.

# CharacterList = [
#     {"name" : "Guerrier", "health" : 100, "power_defense" : 10, "power_attack" : 15 },
#     {"name": "Mage", "health" : 80, "power_defense": 5, "power_attack" : 20 },
#     {"name" : "Archer", "health" : 90, "power_defense": 7, "power_attack" : 18},
#     {"name" : "Voleur", "health" : 85, "power_defense": 8, "power_attack" : 22},
#     {"name" : "Paladin", "health" : 110, "power_defense": 12, "power_attack" : 14},
#     {"name" : "Sorcier", "health" : 70, "power_defense": 3, "power_attack" : 25},
#     {"name" : "Chevalier", "health" : 120,"power_defense": 15, "power_attack" : 17},
#     {"name" : "Moine", "health" : 95, "power_defense": 9, "power_attack" : 19 },
#     {"name" : "Berserker", "health" : 105, "power_defense": 6, "power_attack" : 23},
#     {"name" : "Chasseur", "health" : 100, "power_defense": 11, "power_attack" : 16}
# ]

# EnemyList = [
#     {"name" : "Goblin", "health" : 50, "power_defense" : 5, "power_attack" : 10},
#     {"name" : "Orc", "health" : 120, "power_defense": 8, "power_attack" : 20 },
#     {"name" : "Dragon", "health" : 300, "power_defense": 20, "power_attack" : 35 },
#     {"name" : "Zombie", "health" : 70, "power_defense": 6, "power_attack" : 12 },
#     {"name" : "Troll", "health" : 200, "power_defense": 15, "power_attack" : 25},
#     {"name" : "Spectre",  "health" : 100, "power_defense": 10, "power_attack" : 18},
#     {"name" : "Golem", "health" : 250, "power_defense": 25, "power_attack" : 30 },
#     {"name" : "Vampire", "health" : 150, "power_defense": 12, "power_attack" : 22 },
#     {"name" : "Loup-Garou", "health" : 180, "power_defense": 18, "power_attack" : 28 },
#     {"name" : "Squelette", "health" : 90, "power_defense": 7, "power_attack" : 15 }
# ]