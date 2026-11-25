from models.database import *
from .connect import get_collection

# Dictionnaire des personnages et leurs statistiques
CharacterList = [AlliesDB.__dict__() for AlliesDB in [
	AlliesDB(name="Guerrier", health=100, power_defense=10, power_attack=15),
	AlliesDB(name="Mage", health=80, power_defense=5, power_attack=20),
	AlliesDB(name="Archer", health=90, power_defense=7, power_attack=18),
	AlliesDB(name="Voleur", health=85, power_defense=8, power_attack=22),
	AlliesDB(name="Paladin", health=110, power_defense=12, power_attack=14),
	AlliesDB(name="Sorcier", health=70, power_defense=3, power_attack=25),
	AlliesDB(name="Chevalier", health=120, power_defense=15, power_attack=17),
	AlliesDB(name="Moine", health=95, power_defense=9, power_attack=19),
	AlliesDB(name="Berserker", health=105, power_defense=6, power_attack=23),
	AlliesDB(name="Chasseur", health=100, power_defense=11, power_attack=16),
	AlliesDB(name="Druide", health=90, power_defense=8, power_attack=18),
	AlliesDB(name="Nécromancien", health=75, power_defense=4, power_attack=24),
	AlliesDB(name="Barde", health=85, power_defense=6, power_attack=15),
	AlliesDB(name="Samouraï", health=100, power_defense=10, power_attack=21),
	AlliesDB(name="Templier", health=115, power_defense=14, power_attack=16)
]]


ItemList = [
	Item(name="Potion de soin", item_type="consommable",
	     rarity="commune", effect={"health": 50}, consumable=True),
	Item(name="Épée en fer rouillée", item_type="arme", rarity="commune",
	     effect={"power_attack": 5}, consumable=False),
	Item(name="Bouclier en bois", item_type="armure",
	     rarity="commune", effect={"power_defense": 3}, consumable=False),
	Item(name="Anneau magique", item_type="accessoire", rarity="rare",
	     effect={"power_attack": 10, "power_defense": 5}, consumable=False),
	Item(name="Bouclier en acier", item_type="armure", rarity="rare",
	     effect={"power_defense": 10}, consumable=False),
	Item(name="Arc long", item_type="arme", rarity="rare",
	     effect={"power_attack": 12}, consumable=False),
	Item(name="Dague empoisonnée", item_type="arme", rarity="épique",
	     effect={"power_attack": 20}, consumable=False),
	Item(name="Bouclier en mithril", item_type="armure", rarity="épique",
	     effect={"power_defense": 20}, consumable=False),
	Item(name="Excalibur", item_type="arme", rarity="légendaire",
	     effect={"power_attack": 150, "power_defense": -50}, consumable=False),
	Item(name="Cape d'invisibilité", item_type="armure", rarity="épique",
	     effect={"power_defense": 20}, consumable=False),
	Item(name="Bottes de vitesse", item_type="armure", rarity="rare",
	     effect={"power_defense": 5, "power_attack": 5}, consumable=False),
	Item(name="Lame Vorpaline", item_type="arme", rarity="légendaire",
	     effect={"power_attack": 200, "power_defense": -500}, consumable=False),
	Item(name="Grande potion de soin", item_type="consommable",
	     rarity="rare", effect={"health": 150}, consumable=True),
	Item(name="Élixir de force", item_type="consommable",
	     rarity="rare", effect={"power_attack": 10}, consumable=True),
	Item(name="Hache de guerre", item_type="arme", rarity="rare",
	     effect={"power_attack": 15}, consumable=False),
	Item(name="Casque en fer", item_type="armure", rarity="commune",
	     effect={"power_defense": 4}, consumable=False),
	Item(name="Amulette du dragon", item_type="accessoire", rarity="épique",
	     effect={"power_attack": 15, "power_defense": 15}, consumable=False),
	Item(name="Bâton de l'archimage", item_type="arme", rarity="légendaire",
	     effect={"power_attack": 120, "health": 50}, consumable=False)
]
ItemListDict = [Item.__dict__() for Item in ItemList]


RarityList = [Rarity.__dict__() for Rarity in [
	Rarity(name="commune", drop_rate=0.7),
	Rarity(name="rare", drop_rate=0.25),
	Rarity(name="épique", drop_rate=0.04),
	Rarity(name="légendaire", drop_rate=0.01)
]]

ScoresList = [ScoreDB.__dict__() for ScoreDB in [
	ScoreDB(player_name="Player1", score=100),
	ScoreDB(player_name="Player2", score=200),
	ScoreDB(player_name="Player3", score=150)
]]

EnemyList = [
	MonsterDB(name="Goblin", health=50, power_defense=5, power_attack=10,
	          dropable=[ItemList[0], ItemList[1]]),
	MonsterDB(name="Orc", health=120, power_defense=8, power_attack=20,
	          dropable=[ItemList[1], ItemList[2]]),
	MonsterDB(name="Dragon", health=300, power_defense=20,
	          power_attack=35, dropable=[ItemList[2], ItemList[8], ItemList[11]]),
	MonsterDB(name="Zombie", health=70, power_defense=6, power_attack=12,
	          dropable=[ItemList[0], ItemList[2]]),
	MonsterDB(name="Troll", health=200, power_defense=15,
	          power_attack=25, dropable=[ItemList[1], ItemList[4]]),
	MonsterDB(name="Spectre", health=100, power_defense=10,
	          power_attack=18, dropable=[ItemList[3], ItemList[9]]),
	MonsterDB(name="Golem", health=250, power_defense=25,
	          power_attack=30, dropable=[ItemList[4], ItemList[7]]),
	MonsterDB(name="Vampire", health=150, power_defense=12,
	          power_attack=22, dropable=[ItemList[5], ItemList[6]]),
	MonsterDB(name="Loup-Garou", health=180, power_defense=18,
	          power_attack=28, dropable=[ItemList[6], ItemList[10]]),
	MonsterDB(name="Squelette", health=90, power_defense=7,
	          power_attack=15, dropable=[ItemList[0], ItemList[1]]),
	MonsterDB(name="Araignée géante", health=80, power_defense=6,
	          power_attack=14, dropable=[ItemList[0], ItemList[15]]),
	MonsterDB(name="Minotaure", health=220, power_defense=16,
	          power_attack=27, dropable=[ItemList[14], ItemList[12]]),
	MonsterDB(name="Liche", health=200, power_defense=14,
	          power_attack=32, dropable=[ItemList[13], ItemList[17]]),
	MonsterDB(name="Hydre", health=280, power_defense=19,
	          power_attack=33, dropable=[ItemList[16], ItemList[8]]),
	MonsterDB(name="Gargouille", health=160, power_defense=22,
	          power_attack=20, dropable=[ItemList[4], ItemList[15]])
]
EnemyListDict = [MonsterDB.__dict__() for MonsterDB in EnemyList]


VagueList = [VagueDB.__dict__() for VagueDB in [
	VagueDB(start_number=1, end_number=5, monsters=[EnemyList[0], EnemyList[1]]),
	VagueDB(start_number=6, end_number=10, monsters=[EnemyList[3], EnemyList[9]]),
	VagueDB(start_number=11, end_number=15,
	        monsters=[EnemyList[4], EnemyList[5]]),
	VagueDB(start_number=16, end_number=20,
	        monsters=[EnemyList[6], EnemyList[7]]),
	VagueDB(start_number=21, end_number=25, monsters=[EnemyList[8]]),
	VagueDB(start_number=26, end_number=30, monsters=[EnemyList[2]]),
]]


DifficultyList = [difficulty.__dict__() for difficulty in [
	Difficulty(lap=1, health_multiplier=1.0, attack_multiplier=1.0,
	           defense_multiplier=1.0, item_multiplier=1.0),
	Difficulty(lap=2, health_multiplier=1.2, attack_multiplier=1.1,
	           defense_multiplier=1.1, item_multiplier=1.0),
	Difficulty(lap=3, health_multiplier=1.5, attack_multiplier=1.3,
	           defense_multiplier=1.2, item_multiplier=1.0),
	Difficulty(lap=4, health_multiplier=1.8, attack_multiplier=1.5,
	           defense_multiplier=1.35, item_multiplier=1.1),
	Difficulty(lap=5, health_multiplier=2.2, attack_multiplier=1.8,
	           defense_multiplier=1.5, item_multiplier=1.2),
	Difficulty(lap=6, health_multiplier=2.7, attack_multiplier=2.1,
	           defense_multiplier=1.7, item_multiplier=1.3),
	Difficulty(lap=7, health_multiplier=3.3, attack_multiplier=2.5,
	           defense_multiplier=1.9, item_multiplier=1.4),
	Difficulty(lap=8, health_multiplier=4.0, attack_multiplier=3.0,
	           defense_multiplier=2.2, item_multiplier=1.5),
	Difficulty(lap=9, health_multiplier=5.0, attack_multiplier=3.6,
	           defense_multiplier=2.5, item_multiplier=1.6),
	Difficulty(lap=10, health_multiplier=6.0, attack_multiplier=4.2,
	           defense_multiplier=2.8, item_multiplier=1.8)
]]
# print("Initializing database...")
# client: pymongo.MongoClient = pymongo.MongoClient(os.getenv("MONGO_URL"))
# print("Connected to MongoDB.")
# print("Selecting database...")
# database = client["game_db"]
# print("Database selected.")


# print("Selecting collections...")
SavesList = [save.__dict__() for save in [
	SaveDB(
		player_name="Player1",
		score=100,
		equipe=[
			CharacterSaveDB(name="Guerrier", health=100, equipement=[
			                ItemList[1], ItemList[2]]),
			CharacterSaveDB(name="Mage", health=80, equipement=[ItemList[3]]),
			CharacterSaveDB(name="Archer", health=90, equipement=[ItemList[5]])
		],
		monsters=[
			MonsterSaveDB(name="Goblin", health=50),
			MonsterSaveDB(name="Orc", health=120)
		],
		inventaire=[ItemList[0], ItemList[0]]
	),
	SaveDB(
		player_name="Player2",
		score=200,
		equipe=[
			CharacterSaveDB(name="Paladin", health=110, equipement=[ItemList[4]]),
			CharacterSaveDB(name="Sorcier", health=60, equipement=[ItemList[16]]),
			CharacterSaveDB(name="Voleur", health=85, equipement=[ItemList[6]])
		],
		monsters=[
			MonsterSaveDB(name="Troll", health=150),
			MonsterSaveDB(name="Spectre", health=100)
		],
		inventaire=[ItemList[12], ItemList[13]]
	),
	SaveDB(
		player_name="Player3",
		score=150,
		equipe=[
			CharacterSaveDB(name="Chevalier", health=120, equipement=[
			                ItemList[7], ItemList[15]]),
			CharacterSaveDB(name="Druide", health=90, equipement=[ItemList[10]])
		],
		monsters=[
			MonsterSaveDB(name="Zombie", health=70),
			MonsterSaveDB(name="Squelette", health=45)
		],
		inventaire=[ItemList[0]]
	)
]]

# Characters.drop()
# Monsters.drop()
# Scores.drop()
# difficulty.drop()
# Vagues.drop()
# Items.drop()
# rarities.drop()
# Saves.drop()

def insert_documents(collection, documents):
    if collection.count_documents({}) == 0:
        print(f"Inserting documents into {collection.name}...")
        collection.insert_many(documents)
    else:
        print(f"Collection {collection.name} already has documents. Skipping insertion.")


def initialize_database():
    CharactersConfig = get_collection("config")
    Scores = get_collection("scores")
    difficulty = get_collection("difficulty")
    Vagues = get_collection("vagues")
    Items = get_collection("items")
    rarities = get_collection("rarities")
    Saves = get_collection("saves")

    insert_documents(CharactersConfig, CharacterList)
    insert_documents(CharactersConfig, EnemyListDict)
    insert_documents(Scores, ScoresList)
    insert_documents(difficulty, DifficultyList)
    insert_documents(Vagues, VagueList)
    insert_documents(Items, ItemListDict)
    insert_documents(rarities, RarityList)
    insert_documents(Saves, SavesList)