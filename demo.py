"""Démo manuelle des vues : python demo_vues.py (depuis le dossier JEU2B).

Les données sont écrites en dur, MongoDB n'est pas nécessaire.
"""
from models.affichage import Affichage
#from game_classes import Character, Consumable, Enemy, Equipable
from models.character import Character, Enemy
from models.item import Consumable, Equipable
#from model import CharacterSaveDB, MonsterSaveDB, SaveDB, ScoreDB
from models.database import CharacterSaveDB, MonsterSaveDB, SaveDB, ScoreDB
from models.vue import (
	VueChargerSauvegarde,
	VueChoixCible,
	VueEcranTitre,
	VueGameOver,
	VueInfoTour,
	VueInventaire,
	VueLeaderboard,
	VueQuitter,
	VueSelectionCibleObjet,
	VueSelectionEquipe,
	VueTourJoueur,
)

# ===== Objets =====
potion = Consumable(
	name="Potion de soin", description="Restaure 50 PV",
	drop_rate=0.7, rarity="commune", item_type="consommable", effect={"health": 50})
elixir = Consumable(
	name="Élixir de force", description="Augmente l'attaque de 10",
	drop_rate=0.25, rarity="rare", item_type="consommable", effect={"power_attack": 10})
epee = Equipable(
	name="Épée en fer rouillée", description="Une vieille épée",
	drop_rate=0.7, rarity="commune", item_type="arme", effect={"power_attack": 5})
bouclier = Equipable(
	name="Bouclier en bois", description="Mieux que rien",
	drop_rate=0.7, rarity="commune", item_type="armure", effect={"power_defense": 3})
anneau = Equipable(
	name="Anneau magique", description="Il brille dans le noir",
	drop_rate=0.25, rarity="rare", item_type="accessoire", effect={"power_attack": 10, "power_defense": 5})
excalibur = Equipable(
	name="Excalibur", description="L'épée des rois",
	drop_rate=0.01, rarity="légendaire", item_type="arme", effect={"power_attack": 150, "power_defense": -50})

inventaire = [potion, elixir, anneau, excalibur]

# ===== Équipe : un perso équipé, un blessé, un KO =====
guerrier = Character(name="Guerrier", health=100, max_health=100, power_attack=15, power_defense=10,
                     equipment=[epee, bouclier])
mage = Character(name="Mage", health=35, max_health=80, power_attack=20, power_defense=5)
archer = Character(name="Archer", health=0, max_health=90, power_attack=18, power_defense=7)
team = [guerrier, mage, archer]

personnages_disponibles = [
	Character(name="Voleur", health=85, max_health=85, power_attack=22, power_defense=8),
	Character(name="Paladin", health=110, max_health=110, power_attack=14, power_defense=12),
	Character(name="Sorcier", health=70, max_health=70, power_attack=25, power_defense=3),
	Character(name="Nécromancien", health=75, max_health=75, power_attack=24, power_defense=4),
]

# ===== Ennemis =====
goblin = Enemy(name="Goblin", health=50, max_health=50, power_attack=10, power_defense=5,
               dropable=[potion, epee])
orc = Enemy(name="Orc", health=120, max_health=120, power_attack=20, power_defense=8,
            dropable=[epee, bouclier])
golem = Enemy(name="Golem", health=250, max_health=250, power_attack=30, power_defense=25,
              dropable=[anneau])
ennemis = [goblin, orc, golem]

# ===== Scores et sauvegardes =====
scores = [
	ScoreDB(player_name="Player2", score=200),
	ScoreDB(player_name="Player3", score=150),
	ScoreDB(player_name="Player1", score=100),
]

sauvegardes = [
	SaveDB(
		player_name="Player1",
		score=100,
		equipe=[
			CharacterSaveDB(name="Guerrier", health=100, equipement=[epee, bouclier]),
			CharacterSaveDB(name="Mage", health=80, equipement=[anneau]),
		],
		monsters=[MonsterSaveDB(name="Goblin", health=50),
                    MonsterSaveDB(name="Orc", health=120)],
		inventaire=[potion, potion],
	),
	SaveDB(
		player_name="Player2",
		score=200,
		equipe=[CharacterSaveDB(name="Paladin", health=110, equipement=[])],
		monsters=[MonsterSaveDB(name="Golem", health=150)],
		inventaire=[],
	),
]

evenement = (
	f"{guerrier.name} inflige {guerrier.projected_attack(goblin)} dégâts à {goblin.name}\n"
	f"{orc.name} attaque {mage.name}"
)

# (nom affiché, vue, nombre de choix possibles dans la vue)
DEMOS = [
	("VueEcranTitre", VueEcranTitre(), 4),
	("VueSelectionEquipe", VueSelectionEquipe(team, personnages_disponibles),
	 len(personnages_disponibles)),
	("VueTourJoueur", VueTourJoueur(team, guerrier, ennemis), 3),
	("VueChoixCible", VueChoixCible(team, guerrier, ennemis), len(ennemis)),
	("VueInfoTour", VueInfoTour(team, evenement, ennemis), 1),
	("VueInventaire", VueInventaire(inventaire, team), len(inventaire)),
	("VueInventaire (vide)", VueInventaire([], team), 1),
	("VueSelectionCibleObjet", VueSelectionCibleObjet(potion, team), len(team)),
	("VueGameOver", VueGameOver(), 2),
	("VueLeaderboard", VueLeaderboard(scores), 1),
	("VueLeaderboard (vide)", VueLeaderboard([]), 1),
	("VueChargerSauvegarde", VueChargerSauvegarde(sauvegardes), len(sauvegardes)),
	("VueChargerSauvegarde (vide)", VueChargerSauvegarde([]), 1),
	("VueQuitter", VueQuitter(), 1),
]


def main():
	noms = [nom for nom, _, _ in DEMOS] + ["Quitter la démo"]

	def menu(index: int):
		return Affichage.create_select_box(
			titre="Démo des vues",
			items=noms,
			index=index,
			box_color="cyan",
			text_color="white",
			hover_color="yellow"
		)

	Affichage.console.print(
		"[dim]↑/↓ naviguer • ⏎ ouvrir une vue, puis ⏎ pour revenir au menu • Ctrl+C quitter[/dim]")
	try:
		Affichage.demander_input("Appuyez sur Entrée pour commencer la démo...")
		while True:
			choix = Affichage.display_vue(menu, len(noms))
			if choix is None or choix == len(DEMOS):
				print("Esc ou Ctrl+C détecté, sortie de la démo.")
				break
			nom, vue, max_index = DEMOS[choix]
			resultat = Affichage.display_vue(vue, max_index)
			Affichage.console.print(f"{nom} → index retourné : {resultat}")
	except KeyboardInterrupt:
		print("Ctrl+C détecté, sortie de la démo.")
		pass


if __name__ == "__main__":
	main()