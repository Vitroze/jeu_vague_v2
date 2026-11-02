# Afficher le menu
# Lister les différents options :
#   1. Configurer : Function
#   2. Joueur : Function (Uniquement celui-ci fonctionnera pour l'instant)
#   3. Score : Function
#   4. Quitter (Option mise par défaut)

# Boucle (Tant que l'option n'est pas valide):
#   Demander à l'utilisateur l'option qu'il souhaite choisir via son numéro d'identifiant
#   Vérifier si l'option du joueur est valide
#       - Vérifier que c'est un nombre
#       - Vérifier que ce nombre rentre dans les options
#   Si la valeur est vrai alors on casse la boucle et on exécute la fonction
#   Sinon on redemande

from function.utils import *

def fake_call():
    """Fonction pour le test"""
    pass

options = [
    {
        "name": "Configurer",
        "callback": fake_call,
    },
    {
        "name": "Jouer",
        "callback": fake_call,
    },
    {
        "name": "Score",
        "callback": fake_call,
    }
]

MAX_TEAM = 1

example_character = [
    {
        "name": "Antagoniste",
        "health": 100,
        "power_attack": 20,
        "power_defense": 10,
        "is_ennemy": True,
    },
    {
        "name": "Vrai gentil",
        "health": 92,
        "power_attack": 30,
        "power_defense": 4,
    }
]

def show_menu():
    clear()

    id = 0
    for option in options:
        print(f"{id}. {option["name"]}")
        id += 1

    value = request_option(options)
    options[value]["callback"]()

print(show_menu())
print(choice_valid_by_key(8, options))