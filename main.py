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

from function.game import play
from function.utils import *
from database.connect import connect as connect_db

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

if __name__ == "__main__":
    clear()
    connect_db()
    show_menu()