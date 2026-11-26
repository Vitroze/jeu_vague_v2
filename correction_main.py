import builtins
from time import sleep
import enum
import pymongo
import os
import random

from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align


TEAM_SIZE = 3

TOP_SCORES_COUNT = 3

# _print = builtins.print


# def print(*args, **kwargs):
# _print(*args, **kwargs)
# sleep(0.5)


# Ouvrir DB

# BOUCLE INFINI
# 	Faire choisir utilisateur
# 		recuperer un choix valide (message, options, erreur)
# 			tant que INFINI
# 				Afficher les options
# 				demander un choix
# 				si choix est valid
# 					renvoyer le choix
# 				erreur()
# 			Validite:
# 				verifier que le choix est un entier
# 				verifier que le choix est dans un interval

class Joueur:
	def __init__(self, name):
		self.name = name
		self.waves = 0
		self.actual_wave = 0

	def to_db_score(self):
		return {"player_name": self.name, "waves": self.waves}


def afficher_score(joueur):
	print(f"Score de {joueur.name}: {joueur.waves}")


def creer_joueur(db):
	nom_joueur = recuperer_nom_valide(db)

	return Joueur(nom_joueur)


def recuperer_nom_valide(db):
	while True:
		nom = input("Entrez le nom du joueur: ")
		nom = nom.strip()
		if est_nom_valide(nom, db):
			return nom
		print("Nom invalide ou déjà utilisé, veuillez réessayer.")


def est_nom_valide(nom, db):
	if len(nom) < 3 or len(nom) > 20:
		return False
	if not est_nom_unique(nom, db):
		return False
	return True


def est_nom_unique(nom, db):
	if db["scores"].find_one({"player_name": nom}):
		return False
	return True


# 				Creer une equipe
# 					recuperer perso depuis la DB
# 					Boucle tant que l'equipe n'est pas complete
# 						Afficher equipe
# 						creer la liste des persos dispo (persos, team)
# 						recuperer un choix valide (persos dispos)
# 						Ajouter le perso choisi a l'equipe
def creer_equipe(db):
	persos_db = recuperer_persos_db(db)
	equipe = []
	while not est_equipe_complete(equipe):
		# afficher_equipe(equipe)
		persos_dispo = creer_liste_persos_dispo(persos_db, equipe)
		choix = get_perso_choice(persos_dispo)
		equipe.append(persos_dispo[choix - 1])
	return equipe


def creer_liste_persos_dispo(persos_db, equipe):
	persos_dispo = persos_db.copy()
	for perso in equipe:
		if perso in persos_dispo:
			persos_dispo.remove(perso)
	return persos_dispo


def afficher_equipe(equipe):
	for i in range(TEAM_SIZE):
		if i < len(equipe):
			print(f"{i + 1}. {create_perso_message(equipe[i])}")
		else:
			print(f"{i + 1}. [Vide]")


def est_equipe_complete(equipe):
	return len(equipe) >= TEAM_SIZE


def recuperer_persos_db(db):
	return list(db["characters"].find())


def create_perso_message(perso):
	return f"{perso['name']} - ATK : {perso['attack']} - HP : {perso['hp']} - DEF : {perso['defense']}"


def create_persos_message(persos):
	message = "Choisissez un perso parmi les suivants:"
	return message


def get_perso_choice(persos):
	message = create_persos_message(persos)
	persos_choice = [create_perso_message(perso) for perso in persos]
	choice = get_valid_choice(message, persos_choice, error_message_choice)
	return choice


def recuperer_monstres_db(db):
	return list(db["monsters"].find())


def est_entite_en_vie(entite):
	return entite["hp"] > 0


def est_equipe_en_vie(equipe):
	for membre in equipe:
		if est_entite_en_vie(membre):
			return True
	return False


def selectionner_monstre_aleatoire(monstres):
	import random
	return random.choice(monstres)


# lancer vague (equipe, monstre)
# 	Boucle tant que monstre et equipe sont en vie
# 		recuperer liste des membres de l'equipe en vie
# 		equipe attaque monstre
# 			Pour chaque membre de l'equipe en vie
# 				attaque monstre
# 		monstre attaque equipe
# 			selectionner une cible
# 			attaquer cible
# 		afficher les evenements du tour
# 			Afficher Etat des entites
# 				Afficher equipe
# 				Afficher Monstre
# 			Affiche les evenements
# 			Afficher Etat des entites
# 	retourner est equipe en vie ?

def recuperer_membres_en_vie(equipe):
	membres_en_vie = []
	for membre in equipe:
		if est_entite_en_vie(membre):
			membres_en_vie.append(membre)
	return membres_en_vie


def equipe_attaque_monstre(membres_en_vie, monstre):
	evenements = []
	for membre in membres_en_vie:
		if est_entite_en_vie(monstre):
			evenements.append({"message": infliger_degats(membre, monstre),
			                  "team": copy_team(membres_en_vie), "monster": copy_entity(monstre)})
	return evenements


def choose_target_in_team(equipe):
	return random.choice(equipe)


def infliger_degats(atk, defn):
	degats = max(atk["attack"] - defn["defense"], 1)
	defn["hp"] = max(defn["hp"] - degats, 0)
	return f"{atk['name']} inflige {degats} degats a {defn['name']}"


def copy_entity(entite):
	import copy
	return copy.deepcopy(entite)


def copy_team(equipe):
	return [copy_entity(membre) for membre in equipe]


def monstre_attaque_equipe(monstre, equipe):
	evenements = []
	if not est_entite_en_vie(monstre):
		return []
	membres_en_vie = recuperer_membres_en_vie(equipe)
	target = choose_target_in_team(membres_en_vie)
	evenements.append({"message": infliger_degats(monstre, target),
	                  "monster": copy_entity(monstre), "team": copy_team(equipe)})
	return evenements


def lancer_vague(joueur, equipe, monstre):
	while est_entite_en_vie(monstre) and est_equipe_en_vie(equipe):
		# TODO: Affichage RICH
		evenements = []

		membres_en_vie = recuperer_membres_en_vie(equipe)

		evenements += equipe_attaque_monstre(membres_en_vie, monstre)
		evenements += monstre_attaque_equipe(monstre, equipe)

		afficher_evenements(joueur, evenements)

		# input("")

	return est_equipe_en_vie(equipe)


def creer_titre_tour(player):
	Title = f"Tour de {player.name} - Vague {player.actual_wave}"
	en_tete = Panel(
		Align.center(Title, style=f"bold blue"),
		border_style="blue"
	)
	return en_tete


def creer_text_equipe(equipe):
	return "\n".join([f"{membre['name']} - HP: {membre['hp']}" for membre in equipe])


def creer_team_panel(equipe):
	text_equipe = creer_text_equipe(equipe)
	col_team = Panel(text_equipe, title="🟢 Equipe",
	                 border_style="green", expand=True)
	return col_team


def creer_text_monstre(monstre):
	return f"{monstre['name']} - HP: {monstre['hp']}"


def creer_monstre_panel(monstre):
	text_monstre = creer_text_monstre(monstre)
	col_monstre = Panel(text_monstre, title="🔴 Monstre",
	                    border_style="red", expand=True)
	return col_monstre


console = Console()


def creer_infos_panel(evenement):
	message = evenement["message"]
	panel = Panel(message, title="Infos", border_style="yellow", expand=True)
	return panel


def afficher_evenements(player, evenements):
	titre_tour = creer_titre_tour(player)
	for evenement in evenements:
		clear_console()

		team = creer_team_panel(evenement["team"])
		monster = creer_monstre_panel(evenement["monster"])
		infos = creer_infos_panel(evenement)
		console.print(titre_tour)
		console.print(Columns([team, infos, monster]))

		sleep(2)


def lancer_combat_a_mort(db, joueur, equipe):
	monstres = recuperer_monstres_db(db)
	joueur.actual_wave = 1
	while est_equipe_en_vie(equipe):
		monstre = selectionner_monstre_aleatoire(monstres)
		victoire = lancer_vague(joueur, equipe, monstre)
		if victoire:
			joueur.actual_wave += 1
	return joueur.actual_wave


def enregistrer_score(db, score):
	db.scores.insert_one(score)


def lancer_jeu(db):
	joueur = creer_joueur(db)

	while True:
		equipe = creer_equipe(db)
		waves = lancer_combat_a_mort(db, joueur, equipe)
		joueur.waves = waves
		afficher_score(joueur)
		afficher_leaderboard_joueur(db, joueur.to_db_score())
		if not replay():
			break
	enregistrer_score(db, joueur.to_db_score())


def replay():
	choice = get_valid_choice("Voulez-vous rejouer ?\n1. Oui\n2. Non\nEntrez votre choix: ",
                           ["1. Oui", "2. Non"], error_message_choice)
	return choice == 1


def clear_console():
    # 'nt' correspond à Windows, 'posix' correspond à Linux et macOS
    os.system('cls' if os.name == 'nt' else 'clear')


MENU = [
	"Lancer Jeu",
	"Afficher LeaderBoard",
	"Quitter"
]


def error_message_choice():
	print("Choix invalide, veuillez choisir une option valide")


def create_menu_message():
	message = "Entrez votre choix: "
	return message


def get_valid_choice(message, options, error_message):
	clear_console()
	from InquirerPy import inquirer
	choice = inquirer.select(
		message=message,
		choices=options,
	).execute()
	return options.index(choice) + 1


def is_valid(choice, options):

	if not choice.isdigit():
		return False

	choice = int(choice)

	if choice < 1 or choice > len(options):
		return False

	return True


def get_menu_choice():
	message = create_menu_message()
	choice = get_valid_choice(message, MENU, error_message_choice)
	return choice


client = pymongo.MongoClient(os.getenv("MONGO_URL"))


def connect_db():
	db = client["game_db"]
	return db


def main():
	db = connect_db()
	while True:
		choice = get_menu_choice()
		lancer_processus(choice, db)


def close_db():
	client.close()


def lancer_processus(choice, db):
	if choice == 1:
		lancer_jeu(db)
	elif choice == 2:
		afficher_leaderboard(db)
	elif choice == 3:
		close_db()
		print("Fermeture du programme")
		exit()
	else:
		print("Choix invalide")


# 		2 : Afficher LeaderBoard (DB)
# 			Recuperer les scores
# 			Trier les scores
# 			Recuperer les 3 plus grands scores [-3:-1]
# 			Afficher les scores
# 				pour score dans scores
# 					Afficher score


def get_sorted_scores(list_scores):
	scores = sorted(list_scores, key=lambda x: x["waves"], reverse=True)
	return scores


def afficher_scores(scores):
	for score in scores:
		print(f"{score['player_name']} : {score['waves']}")
	sleep(0.5)


def get_top_scores(list_scores):
	scores = get_sorted_scores(list_scores)
	return scores[:TOP_SCORES_COUNT]


def get_score_db(db):
	return list(db.scores.find())


def afficher_leaderboard(db):
	scores_db = get_score_db(db)
	scores = get_top_scores(scores_db)
	afficher_scores(scores)


def afficher_leaderboard_joueur(db, player):
	scores_db = get_score_db(db)
	scores_db.append(player)
	scores = get_top_scores(scores_db)
	afficher_scores(scores)


main()