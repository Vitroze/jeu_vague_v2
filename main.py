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

from function.main_menu import show_menu
from function.utils import clear
from database.connect import connect as connect_db

def main():
    clear()
    connect_db()
    show_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass