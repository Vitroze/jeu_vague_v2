from models.database import *
from .connect import get_collection
from models.item import Item

# Dictionnaire des personnages et leurs statistiques
CharacterList = [AlliesDB.__dict__() for AlliesDB in [
	AlliesDB(name="Guerrier", health=105, power_defense=10, power_attack=17),
	AlliesDB(name="Mage", health=80, power_defense=5, power_attack=23),
	AlliesDB(name="Archer", health=90, power_defense=7, power_attack=20),
	AlliesDB(name="Voleur", health=85, power_defense=7, power_attack=23),
	AlliesDB(name="Paladin", health=115, power_defense=12, power_attack=16),
	AlliesDB(name="Sorcier", health=75, power_defense=4, power_attack=25),
	AlliesDB(name="Chevalier", health=120, power_defense=14, power_attack=17),
	AlliesDB(name="Moine", health=95, power_defense=9, power_attack=19),
	AlliesDB(name="Berserker", health=100, power_defense=6, power_attack=24),
	AlliesDB(name="Chasseur", health=95, power_defense=9, power_attack=19),
	AlliesDB(name="Druide", health=95, power_defense=8, power_attack=18),
	AlliesDB(name="Nécromancien", health=80, power_defense=5, power_attack=24),
	AlliesDB(name="Barde", health=90, power_defense=7, power_attack=17),
	AlliesDB(name="Samouraï", health=95, power_defense=9, power_attack=22),
	AlliesDB(name="Templier", health=115, power_defense=13, power_attack=17)
]]

ItemList = [
	Item.create(name="Potion de soin", item_type="consommable",
	     rarity="commune", effect={"health": 35}, consumable=True),
	Item.create(name="Épée en fer rouillée", item_type="arme", rarity="commune",
	     effect={"power_attack": 4}, consumable=False),
	Item.create(name="Bouclier en bois", item_type="armure",
	     rarity="commune", effect={"power_defense": 3}, consumable=False),
	Item.create(name="Anneau magique", item_type="accessoire", rarity="rare",
	     effect={"power_attack": 6, "power_defense": 4}, consumable=False),
	Item.create(name="Bouclier en acier", item_type="armure", rarity="rare",
	     effect={"power_defense": 6}, consumable=False),
	Item.create(name="Arc long", item_type="arme", rarity="rare",
	     effect={"power_attack": 8}, consumable=False),
	Item.create(name="Dague empoisonnée", item_type="arme", rarity="épique",
	     effect={"power_attack": 12}, consumable=False),
	Item.create(name="Bouclier en mithril", item_type="armure", rarity="épique",
	     effect={"power_defense": 9}, consumable=False),
	Item.create(name="Excalibur", item_type="arme", rarity="légendaire",
	     effect={"power_attack": 18, "power_defense": -3}, consumable=False),
	Item.create(name="Cape d'invisibilité", item_type="armure", rarity="épique",
	     effect={"power_defense": 9}, consumable=False),
	Item.create(name="Bottes de vitesse", item_type="armure", rarity="rare",
	     effect={"power_defense": 3, "power_attack": 3}, consumable=False),
	Item.create(name="Lame Vorpaline", item_type="arme", rarity="légendaire",
	     effect={"power_attack": 22, "power_defense": -5}, consumable=False),
	Item.create(name="Grande potion de soin", item_type="consommable",
	     rarity="rare", effect={"health": 75}, consumable=True),
	Item.create(name="Élixir de force", item_type="consommable",
	     rarity="rare", effect={"power_attack": 6}, consumable=True),
	Item.create(name="Hache de guerre", item_type="arme", rarity="rare",
	     effect={"power_attack": 9}, consumable=False),
	Item.create(name="Casque en fer", item_type="armure", rarity="commune",
	     effect={"power_defense": 4}, consumable=False),
	Item.create(name="Amulette du dragon", item_type="accessoire", rarity="épique",
	     effect={"power_attack": 9, "power_defense": 7}, consumable=False),
	Item.create(name="Bâton de l'archimage", item_type="arme", rarity="légendaire",
	     effect={"power_attack": 16, "health": 20}, consumable=False)
]
ItemListDict = [Item.__dict__() for Item in ItemList]


RarityList = [Rarity.__dict__() for Rarity in [
	Rarity(name="commune", drop_rate=0.5),
	Rarity(name="rare", drop_rate=0.2),
	Rarity(name="épique", drop_rate=0.05),
	Rarity(name="légendaire", drop_rate=0.01)
]]

ScoresList = [ScoreDB.__dict__() for ScoreDB in [
	ScoreDB(player_name="Player1", score=100),
	ScoreDB(player_name="Player2", score=200),
	ScoreDB(player_name="Player3", score=150)
]]

EnemyList = [
	MonsterDB(name="Goblin", health=90, power_defense=4, power_attack=10,
	          dropable=[ItemList[0], ItemList[1]]),
	MonsterDB(name="Orc", health=160, power_defense=8, power_attack=16,
	          dropable=[ItemList[1], ItemList[2]]),
	MonsterDB(name="Dragon", health=450, power_defense=18,
	          power_attack=30, dropable=[ItemList[2], ItemList[8], ItemList[11]]),
	MonsterDB(name="Zombie", health=100, power_defense=5, power_attack=11,
	          dropable=[ItemList[0], ItemList[2]]),
	MonsterDB(name="Troll", health=210, power_defense=13,
	          power_attack=20, dropable=[ItemList[1], ItemList[4]]),
	MonsterDB(name="Spectre", health=160, power_defense=8,
	          power_attack=17, dropable=[ItemList[3], ItemList[9]]),
	MonsterDB(name="Golem", health=280, power_defense=18,
	          power_attack=24, dropable=[ItemList[4], ItemList[7]]),
	MonsterDB(name="Vampire", health=200, power_defense=10,
	          power_attack=22, dropable=[ItemList[5], ItemList[6]]),
	MonsterDB(name="Loup-Garou", health=240, power_defense=13,
	          power_attack=23, dropable=[ItemList[6], ItemList[10]]),
	MonsterDB(name="Squelette", health=120, power_defense=6,
	          power_attack=13, dropable=[ItemList[0], ItemList[1]]),
	MonsterDB(name="Araignée géante", health=100, power_defense=5,
	          power_attack=12, dropable=[ItemList[0], ItemList[15]]),
	MonsterDB(name="Minotaure", health=260, power_defense=15,
	          power_attack=24, dropable=[ItemList[14], ItemList[12]]),
	MonsterDB(name="Liche", health=230, power_defense=12,
	          power_attack=25, dropable=[ItemList[13], ItemList[17]]),
	MonsterDB(name="Hydre", health=380, power_defense=17,
	          power_attack=28, dropable=[ItemList[16], ItemList[8]]),
	MonsterDB(name="Gargouille", health=190, power_defense=16,
	          power_attack=18, dropable=[ItemList[4], ItemList[15]])
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
	Difficulty(lap=2, health_multiplier=1.1, attack_multiplier=1.05,
	           defense_multiplier=1.0, item_multiplier=1.0),
	Difficulty(lap=3, health_multiplier=1.2, attack_multiplier=1.1,
	           defense_multiplier=1.05, item_multiplier=1.0),
	Difficulty(lap=4, health_multiplier=1.3, attack_multiplier=1.15,
	           defense_multiplier=1.05, item_multiplier=1.05),
	Difficulty(lap=5, health_multiplier=1.45, attack_multiplier=1.2,
	           defense_multiplier=1.1, item_multiplier=1.05),
	Difficulty(lap=6, health_multiplier=1.6, attack_multiplier=1.25,
	           defense_multiplier=1.1, item_multiplier=1.1),
	Difficulty(lap=7, health_multiplier=1.8, attack_multiplier=1.3,
	           defense_multiplier=1.15, item_multiplier=1.1),
	Difficulty(lap=8, health_multiplier=2.0, attack_multiplier=1.35,
	           defense_multiplier=1.15, item_multiplier=1.15),
	Difficulty(lap=9, health_multiplier=2.2, attack_multiplier=1.4,
	           defense_multiplier=1.2, item_multiplier=1.15),
	Difficulty(lap=10, health_multiplier=2.5, attack_multiplier=1.45,
	           defense_multiplier=1.2, item_multiplier=1.2)
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
		team=[
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
		team=[
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
		team=[
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

	insert_documents(CharactersConfig, CharacterList + EnemyListDict) # Un seul appel : insert_documents ignore une collection déjà remplie
	insert_documents(Scores, ScoresList)
	insert_documents(difficulty, DifficultyList)
	insert_documents(Vagues, VagueList)
	insert_documents(Items, ItemListDict)
	insert_documents(rarities, RarityList)
	insert_documents(Saves, SavesList)