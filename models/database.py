from typing import Dict, List
from dataclasses import dataclass

class CharacterDB:
    def __init__(self, name: str, health: int, power_defense: int, power_attack: int, is_ennemy: bool):
        self.name = name
        self.health = health
        self.power_defense = power_defense
        self.power_attack = power_attack
        self.is_ennemy = is_ennemy

    def __dict__(self):
        return {
            "name": self.name,
            "health": self.health,
            "power_defense": self.power_defense,
            "power_attack": self.power_attack,
            "is_ennemy": self.is_ennemy
        }

class AlliesDB(CharacterDB):

    def __init__(self, name: str, health: int, power_defense: int, power_attack: int):
        super().__init__(name, health, power_defense, power_attack, is_ennemy=False)
        self.is_ennemy = False

class MonsterDB(CharacterDB):

    def __init__(self, name: str, health: int, power_defense: int, power_attack: int, dropable: List["Item"]):
        super().__init__(name, health, power_defense, power_attack, is_ennemy=True)
        self.dropable = dropable

    def __dict__(self):
        return {
            "name": self.name,
            "health": self.health,
            "power_defense": self.power_defense,
            "power_attack": self.power_attack,
            "dropable": [item.name for item in self.dropable],
            "is_ennemy": self.is_ennemy
        }

# @dataclass
# class CharacterDB:
#     name: str
#     hp: int
#     defense: int
#     attack: int

#     def __dict__(self):
#         return {
#             "name": self.name,
#             "hp": self.hp,
#             "defense": self.defense,
#             "attack": self.attack,
#             "is_ennemy": False
#         }


# @dataclass
# class MonsterDB:
#     name: str
#     hp: int
#     defense: int
#     attack: int
#     dropable: List["Item"]

#     def __dict__(self):
#         return {
#             "name": self.name,
#             "health": self.hp,
#             "power_defense": self.defense,
#             "power_attack": self.attack,
#             "dropable": [item.name for item in self.dropable],
#             "is_ennemy": True
#         }


@dataclass
class ScoreDB:
    player_name: str
    score: int

    def __dict__(self):
        return {
            "player_name": self.player_name,
            "score": self.score
        }


@dataclass
class CharacterSaveDB:
    name: str
    health: int
    equipement: List["Item"]

    def __dict__(self):
        return {
            "name": self.name,
            "health": self.health,
            "equipement": [item.name for item in self.equipement]
        }


@dataclass
class MonsterSaveDB:
    name: str
    health: int

    def __dict__(self):
        return {
            "name": self.name,
            "health": self.health
        }


@dataclass
class SaveDB:
    player_name: str
    score: int
    equipe: List[CharacterSaveDB]
    monsters: List[MonsterSaveDB]
    inventaire: List["Item"]

    def __dict__(self):
        return {
            "player_name": self.player_name,
            "score": self.score,
            "equipe": [char.__dict__() for char in self.equipe],
            "monsters": [mon.__dict__() for mon in self.monsters],
            "inventaire": [item.name for item in self.inventaire]
        }


@dataclass
class Item:
    name: str
    item_type: str
    rarity: str
    effect: Dict[str, int]
    consumable: bool

    def __dict__(self):
        return {
            "name": self.name,
            "item_type": self.item_type,
            "rarity": self.rarity,
            "effect": self.effect,
            "consumable": self.consumable
        }


@dataclass
class VagueDB:
    start_number: int
    end_number: int
    monsters: List[MonsterDB]

    def __dict__(self):
        return {
            "start_number": self.start_number,
            "end_number": self.end_number,
            "monsters": [mon.__dict__() for mon in self.monsters]
        }


@dataclass
class Difficulty:
    lap: int
    health_multiplier: float
    attack_multiplier: float
    defense_multiplier: float
    item_multiplier: float

    def __dict__(self):
        return {
            "lap": self.lap,
            "health_multiplier": self.health_multiplier,
            "attack_multiplier": self.attack_multiplier,
            "defense_multiplier": self.defense_multiplier,
            "item_multiplier": self.item_multiplier
        }


@dataclass
class Rarity:
    name: str
    drop_rate: float

    def __dict__(self):
        return {
            "name": self.name,
            "drop_rate": self.drop_rate
        }