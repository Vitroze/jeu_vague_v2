from time import sleep

from rich.console import Console
from rich.align import Align
import copy
import os
from random import random
from pymongo import MongoClient
from random import choice
from rich.layout import Layout
LAYOUT = Layout()
console = Console()

TAILLE_MAX_EQUIPE = 3
MENU = ["Jouer", "Leaderboard", "Quitter"]
LAYOUT.split_row(
    Layout(name="left", ratio=2),
    Layout(name="center", ratio=3),  # Le centre sera 3 fois plus grand
    Layout(name="right", ratio=2)   # La droite sera 2 fois plus grande
)


def create_panel(title="", text="", color="yellow"):
	from rich.panel import Panel

	text_color = {"red": {"start": "[red]", "end": "[/red]"},
               "green": {"start": "[green]", "end": "[/green]"},
               "blue": {"start": "[blue]", "end": "[/blue]"},
               "yellow": {"start": "[yellow]", "end": "[/yellow]"}
               }

	return Panel(Align.center(text_color[color]["start"] + text + text_color[color]["end"], vertical="middle"), title=title, border_style=color)

	# CHOIX DU MENU
	# 	liste d'options = MENU
	# 	message = "Veuillez choisir une option :"
	# 	recuperer le choix utilisateur valide depuis une liste d'options
	# 	retourner le choix
	# Lancer processus
	# 	1 - Jeu
	# 	2 - Leaderboard
	# 	3 - Quitter

	# 1 - Jeu
	# ouvrir une connexion a la db
	# demander un pseudo utilisateur
	# recuperer la liste des heros selectionnables
	# creer une equipe
	# lancer le combat a mort
	# enregistrer le resultat du combat

	# Recuperer le choix utilisateur valide depuis une liste d'options (options, message)
	# 	tant que infini
	# 		Afficher les options disponibles
	# 		demander un input (message)
	# 		verifier la validite du choix (choix, 1, len(options))
	# 		si choix valide
	# 			retourner le choix
	#

	# Valider un choix utilisateur (choix, minimum, maximum)
	# 	si pas choix.isdigit()
	# 		retourner False
	# 	converti le choix en entier
	# 	si choix < minimum ou choix > maximum
	# 		retourner False
	# 	retourner True

	# lancer le combat a mort
	# 	vague = 1
	# 	tant que equipe est en vie
	# 		selectionner un monstre pour la vague
	# 		victoire = lancer la vague
	# 		si victoire
	# 			afficher un message de victoire pour la vague
	# 			vague = vague + 1

	# lancer la vague
	# 	tant que monstre est en vie et equipe est en vie
	# 		evenements = tour de vague
	# 		afficher les evenements du tour
	# 	retourne equipe est en vie

	# afficher les evenements du tour
	# 	pour chaque evenement dans la liste des evenements
	# 		afficher l'evenement
	# 	afficher un separateur pour distinguer les tours


def choix_menu():
	# Recuperer le choix utilisateur valide depuis la liste MENU
	message = "Veuillez choisir une option :"
	return get_user_choice_from_options(MENU, message)


def lancer_processus(choix):
	if choix == 1:
		lancer_jeu()
		pass
	elif choix == 2:
		# Afficher le leaderboard
		pass
	elif choix == 3:
		# Quitter le programme
		pass


def main():
	choix = choix_menu()
	lancer_processus(choix)


def afficher_game_over(equipe, score):
	print("Game Over !")
	print(f"Votre équipe a survécu à {score} vagues.")
	print("Statut final de l'équipe :")
	for hero in equipe:
		print(f"{hero['name']} - HP: {hero['hp']}")


def lancer_jeu():
	db = connect_db()
	pseudo = get_username(db)
	heros_disponibles = recuperer_all_heroes(db)
	monstres = recuperer_all_monsters(db)
	equipe = create_team(heros_disponibles)
	score = combat_a_mort(equipe, monstres)
	afficher_game_over(equipe, score)
	enregistrer_resultat_combat(db, pseudo, score)


def enregistrer_resultat_combat(db, pseudo, score):
	db["scores"].insert_one({
		"player_name": pseudo,
		"waves": score
	})


def recuperer_all_heroes(db):
	return list(db["characters"].find())


def recuperer_all_monsters(db):
	return list(db["monsters"].find())


def connect_db():
	client = MongoClient(os.getenv("MONGO_URL"))
	return client["game_db"]


def est_entite_en_vie(entite):
	return entite["hp"] > 0


def est_equipe_en_vie(equipe):
	for hero in equipe:
		if est_entite_en_vie(hero):
			return True
	return False


def selectionner_monstre(monstres):
	monstre_choice = choice(monstres)
	return copy.deepcopy(monstre_choice)


def combat_a_mort(equipe, monstres):
	vague = 1
	while est_equipe_en_vie(equipe):
		monstre = selectionner_monstre(monstres)
		victoire = lancer_vague(equipe, monstre)
		if victoire:
			print(f"Victoire pour la vague {vague} !")
			vague += 1
	return vague


def lancer_vague(equipe, monstre):
	while est_entite_en_vie(monstre) and est_equipe_en_vie(equipe):
		evenements = tour_de_vague(equipe, monstre)
		afficher_evenements(evenements, equipe, monstre)
		sleep(1)
	return est_equipe_en_vie(equipe)


def update_layout(equipePanel, monstrePanel, info_panel):
	global LAYOUT
	LAYOUT["left"].update(equipePanel)
	LAYOUT["right"].update(monstrePanel)
	LAYOUT["center"].update(info_panel)


def afficher_evenements(evenements, equipe, monstre):
	console.clear()
	print("\n\n")

	equipePanel = create_panel("Equipe", "\n".join(
		[f"{hero['name']} - HP: {hero['hp']}" for hero in equipe]), "green")
	monstrePanel = create_panel(
		"Monstre", f"{monstre['name']} - HP: {monstre['hp']}", "red")
	info_panel = create_panel("Evenements", "\n".join(evenements), "yellow")

	update_layout(equipePanel, monstrePanel, info_panel)

	console.print(LAYOUT, height=10)


def afficher_stats(equipe, monstre):
	print("-" * 10 + " Stats " + "-" * 10)
	print("Stats de l'equipe :")
	for hero in equipe:
		if not est_entite_en_vie(hero):
			print(f"{hero['name']} est KO")
			continue
		print(f"{hero['name']} - HP: {hero['hp']}")
	print("Stats du monstre :")
	print(f"{monstre['name']} - HP: {monstre['hp']}")
	print("-" * 30)

# affiche les stats de l'equipe et du monstre
# 	afficher "Stats de l'equipe :"
# 	pour chaque hero dans l'equipe
# 		afficher le nom du hero et ses points de vie
# 	afficher "Stats du monstre :"
# 	afficher le nom du monstre et ses points de vie


def tour_de_vague(equipe, monstre):
	evenements = []
	evenements += tour_utilisateur(equipe, monstre)
	if est_entite_en_vie(monstre):
		evenements += tour_monstre(equipe, monstre)
	return evenements
# tour de vague
# 	Initialiser une liste vide pour les evenements du tour
# 	evenements += Tour Utilisateur
# 	si monstre est en vie
# 		evenements += Tour Monstre
# 	retourner la liste des evenements du tour


def tour_monstre(equipe, monstre):
	evenements = []
	cible = recuperer_cible(equipe)
	degat = attaquer(monstre, cible)
	evenements.append(
		f"{monstre['name']} inflige {degat} degats a {cible['name']}")
	return evenements
# Tour Monstre
# 	recuperer une cible
# 	degat = attaquer la cible
# 	retourner un evenement indiquant que le monstre a inflige des degats a la cible


def attaquer(attacker, cible):
	degat = calculer_degats(attacker, cible)
	if degat > cible["hp"]:
		degat = cible["hp"]
	cible["hp"] -= degat
	return degat
# attaquer la cible
# 	calculer les degats infliges a la cible
# 	si degat > hp cible
# 		degat = hp cible
# 	reduire les points de vie de la cible en fonction des degats
# 	retourner les degats infliges


def calculer_degats(attacker, cible):
	degat = attacker["attack"] - cible["defense"]
	if degat < 1:
		degat = 1
	return degat
# calculer les degats infliges a la cible
# 	degat = attaque - defense cible
# 	si degat < 1
# 		degat = 1
# 	retourner degat

# recuperer une cible
# 	cible_potentielle = recuperer heros en vie de l'equipe
# 	retourner random.choice(cible_potentielle)


def recuperer_cible(equipe):
	cible_potentielle = recuperer_heros_en_vie(equipe)
	return choice(cible_potentielle)


def recuperer_heros_en_vie(equipe):
	heros_en_vie = []
	for hero in equipe:
		if est_entite_en_vie(hero):
			heros_en_vie.append(hero)
	return heros_en_vie


def tour_utilisateur(equipe, monstre):
	evenements = []
	heros_en_vie = recuperer_heros_en_vie(equipe)
	for hero in heros_en_vie:
		evenements += tour_perso_jouable(hero, monstre)
	return evenements
# Tour Utilisateur
# 	Initialiser une liste vide pour les evenements du tour utilisateur
# 	recuperer heros en vie de l'equipe
# 	pour chaque heros en vie
# 		evenements += tour perso jouable
# 	retourner la liste des evenements du tour utilisateur


def tour_perso_jouable(hero, monstre):
	evenements = []
	if est_entite_en_vie(monstre):
		degat = attaquer(hero, monstre)
		evenements.append(
			f"{hero['name']} inflige {degat} degats a {monstre['name']}")
	return evenements
# Tour perso jouable
# 	evenement = []
# 	si monstre est en vie
# 		evenement = attaquer le monstre
# 	retourner l'evenement du tour du perso


def create_team(heroes):
	equipe = []
	while not equipe_est_complete(equipe):
		afficher_equipe_actuelle(equipe)
		heros_dispo = calculer_heros_disponibles(equipe, heroes)
		options = construire_options(heros_dispo)
		choix = get_user_choice_from_options(options, "Choisissez un héros : ")
		selected_hero = copy.deepcopy(heros_dispo[choix - 1])
		equipe.append(selected_hero)
	return equipe
# creer une equipe
# 	Initialiser une liste vide pour l'equipe
# 	Tant que pas equipe est complete
# 		Afficher l'equipe actuelle
# 		calculer la liste des heros encore disponibles
# 		construit mes options
# 		demander un choix valide parmi les options
# 		ajouter le choix a l'equipe
# 	retourner l'equipe complete


def equipe_est_complete(equipe):
	if len(equipe) < TAILLE_MAX_EQUIPE:
		return False
	return True


def hero_to_string(hero):
	return f"{hero['name']} - ATK : {hero['attack']} - HP : {hero['hp']} - DEF : {hero['defense']}"


def construire_options(liste_heros_dispo):
	options = []
	for hero in liste_heros_dispo:
		options.append(hero_to_string(hero))
	return options
# construire mes options(liste_heros_dispo)
# 	Initialiser une liste vide pour les options
# 	Pour chaque hero dans liste_heros_dispo
# 		Construire une string "NOM HERO - ATK : <valeur> - HP : <valeur> - DEF : <valeur>"
# 		Ajouter la string a la liste des options
# 	retourner la liste des options


def calculer_heros_disponibles(equipe, liste_heros):
	heros_disponibles = []
	for hero in liste_heros:
		if hero not in equipe:
			heros_disponibles.append(hero)
	return heros_disponibles

# Calculer la liste des heros encore disponibles ( equipe, liste_heros)
# 	Initialiser une liste vide pour les heros disponibles
# 	pour chaque hero dans liste_heros
# 		si hero n'est pas dans equipe
# 			l'ajouter a la liste des heros disponibles
# 	retourner la liste des heros disponibles


def afficher_personnage(personnage):
	print(hero_to_string(personnage))


def afficher_equipe_actuelle(equipe):
	for i in range(TAILLE_MAX_EQUIPE):
		if i < len(equipe):
			afficher_personnage(equipe[i])
		else:
			print("Vide")
# Afficher l'equipe actuelle
# 	boucler Taille Max de l'equipe
# 		Si un hero est present a cet index
# 			Afficher le hero
# 		Sinon
# 			Afficher "Vide"

# equipe est complete
# 	si la taille de l'equipe < taille maximale
# 		retourner False
# 	retourner True

def est_equipe_complete(equipe):
    return len(equipe) >= TAILLE_MAX_EQUIPE

# recuperer la liste des heros selectionnables
# 	recuperer la liste des heros depuis la database
# 	convertir le resultat en liste
# 	retourner la liste des heros disponibles


def get_username(db):
	while True:
		pseudo = input("Entrez votre pseudo : ").strip()
		if validate_username(pseudo, db):
			return pseudo
		print("Pseudo invalide, veuillez réessayer.")


def validate_username(pseudo, db):
	if len(pseudo) < 3 or len(pseudo) > 20:
		return False
	if pseudo in banned_pseudos:
		return False
	if is_username_in_db(pseudo, db):
		return False
	return True
# demander un pseudo utilisateur
# 	Tant que infini
# 		demander un input pour le pseudo
# 		strip le pseudo pour enlever les espaces superflus
# 		si le pseudo est valide
# 			retourner le pseudo
# 		afficher un message d'erreur


# Valider un pseudo utilisateur (pseudo)
# 	si la taille du pseudo est inférieure à 3 ou supérieure à 20
# 		retourner False
# 	si pseudo present dans banned_pseudos var in []
# 		retourner False
# 	si le pseudo est deja dans la database
# 		retourner False
# 	retourner True

def is_username_in_db(pseudo, db):
	pseudos_in_db = [user["player_name"] for user in db["scores"].find()]
	if pseudo in pseudos_in_db:
		return True
	return False


banned_pseudos = ["admin", "root", "superuser"]


def get_user_choice_from_options(options, message):
	while True:
		print(message)
		for i, option in enumerate(options, start=1):
			print(f"{i}. {option}")
		choix = input("Entrez votre choix : ").strip()
		if validate_user_choice(choix, 1, len(options)):
			return int(choix)
		print("Choix invalide, veuillez réessayer.")


def validate_user_choice(choix, minimum, maximum):
	if not choix.isdigit():
		return False
	choix = int(choix)
	if choix < minimum or choix > maximum:
		return False
	return True


main()


# Afficher Menu
# Recuperer un choix valide parmi les options
#    tant que infini
#        afficher les options numerotees
#             pour chaque option dans enumerate(options, start=1)
#                 afficher {i}. {option}
#        demander un choix a l'utilisateur
#        si le choix est valide
#            retourner le choix valide
#        afficher un message d'erreur

# choix est valide
#    si le choix n'est pas isdigit()
#        retourner False
#    convertir le choix en entier
#    si le choix est inférieur au minimum ou supérieur au maximum
#        retourner False
#    retourner True


def recuperer_choix_utilisateur(options):
	while True:
		afficher_options_numerotees(options)
		choix = input("Entrez votre choix : ")
		if est_choix_valide(choix, 1, len(options)):
			return int(choix)
		print("Choix invalide, veuillez réessayer.")


def afficher_options_numerotees(options):
	for i, option in enumerate(options, start=1):
		print(f"{i}. {option}")


def truc_complexe(choix):
	# requete...

	return True


def est_choix_valide(choix, minimum, maximum):
	validator = [
            lambda x: x.isdigit(),
            lambda x: minimum <= int(x) <= maximum,
            truc_complexe
        ]
	for v in validator:
		if not v(choix):
			return False
	return True


# Lancer le processus choisi

choix = recuperer_choix_utilisateur(["Option 1", "Option 2", "Option 3"])
print(f"Vous avez choisi l'option {choix}")


# Besoin la liste des personnages de la DB
def creer_equipe(liste_personnages_db):
	# creer la variable equipe vide
	equipe = []
	# tant que l'equipe n'est pas complete
	while not est_equipe_complete(equipe):
		#     determiner la liste des personnages disponibles
		personnages_disponibles = determiner_personnages_disponibles(
			liste_personnages_db, equipe)
		#     construire la liste des options a afficher disponibles
		options_affichables = construire_options_affichables(personnages_disponibles)
		#     recuperer un choix valide
		choix = recuperer_choix_utilisateur(options_affichables)
		#     ajouter le personnage choisi a l'equipe index = choix - 1
		equipe.append(personnages_disponibles[choix - 1])
	# retourner l'equipe
	return equipe

# construire la liste des options a afficher disponibles


def construire_options_affichables(personnages_disponibles):
	# creer la liste options
	options = []
	# pour chaque personnage dans personnages_disponibles
	for personnage in personnages_disponibles:
		#    ajouter a la liste : f"{personnage["nom"]} - ATK : {personnage["atk"]} - DEF : {personnage["def"]}"
		options.append(
			f"{personnage['nom']} - ATK : {personnage['atk']} - DEF : {personnage['def']}")
	# retourner la liste des options
	return options

	...


def determiner_personnages_disponibles(liste_personnages_db, equipe):
	# creer la liste des personnages disponibles
	personnages_disponibles = []
	# pour chaque personnage dans la liste des personnages de la DB
	for personnage in liste_personnages_db:
		#     si le personnage n'est pas dans l'equipe
		if personnage not in equipe:
			#         l'ajouter a la liste des personnages disponibles
			personnages_disponibles.append(personnage)
	# renvoyer la liste des personnages disponibles
	return personnages_disponibles