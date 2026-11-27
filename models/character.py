from abc import ABC, abstractmethod
from function.utils import clamp
from models.item import Equipable
from typing import List

class Entity(ABC):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int, is_ennemy: bool = False):
        self.name = name
        self.health = health
        self.max_health = health
        self.power_attack = power_attack
        self.power_defense = power_defense
        self.is_ennemy = is_ennemy
        self.target = None

    def set_health(self, health: int):
        health = max(health, 0)
        self.health = health

    def get_attack_power(self):
        return self.power_attack

    def get_defense_power(self):
        return self.power_defense

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "power_attack": self.power_attack,
            "power_defense": self.power_defense,
            "is_ennemy": self.is_ennemy
        }

    def take_damage(self, amount: int):
        self.set_health(self.health - amount)
        return amount
        # power_attack = other_character.get_attack_power() - self.get_defense_power()
        # power_attack = max(2, power_attack)

        # new_health = self.health - power_attack
        # self.set_health(new_health)

        # if new_health < 1:
        #     return {"message": f"{self.name} a été vaincu par {other_character.name} !"}

        # return {"message": f"{other_character.name} inflige {power_attack} degats a {self.name}"}

    def attack(self, target: "Entity"):
        power_attack = self.get_attack_power() - target.get_defense_power()
        power_attack = max(2, power_attack)

        return target.take_damage(power_attack)

    def is_alive(self):
        return self.health > 0

    def is_death(self):
        return self.health <= 0

    @classmethod
    def is_valid_values_for_character(cls, dict_character: dict)->bool:
        return dict_character.get("name") and dict_character.get("health") and dict_character.get("power_attack") and dict_character.get("power_defense")

    @classmethod
    def create_character(cls, info_character: dict):
        if not Entity.is_valid_values_for_character(info_character):
            return None

        return Entity(
            info_character["name"],
            info_character["health"],
            info_character["power_attack"],
            info_character["power_defense"],
            info_character.get("is_ennemy"),
        )

    def heal(self, amount: int):
        self.health = clamp(self.health + amount, 0, self.max_health)

    @abstractmethod
    def play_turn(self):
        """UML: Play a turn for the entity. This method should be implemented by subclasses."""
        # if not self.target:
        #     return None

        # attack = self.target.take_damage(self)
        # return attack

    def attack_target(self):
        target = self.target
        if not target:
            return None

        attack = target.take_damage(self)
        return attack

    @classmethod
    def create_character(cls, info_character: dict):
        if not Entity.is_valid_values_for_character(info_character):
            return None

        if info_character.get("is_ennemy"):
            return Enemy(
                info_character["name"],
                info_character["health"],
                info_character["power_attack"],
                info_character["power_defense"],
                info_character.get("dropable", []),
            )

        return Character(
            info_character["name"],
            info_character["health"],
            info_character["power_attack"],
            info_character["power_defense"],
        )

class Character(Entity):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int):
        super().__init__(name, health, power_attack, power_defense, is_ennemy=False)
        self.equipments: List[Equipable] = []

    def get_attack_power(self):
        total_attack_power = self.power_attack
        for equipment in self.equipments:
            total_attack_power += equipment.get_attack_bonus()
        return total_attack_power


    def get_defense_power(self):
        total_defense_power = self.power_defense
        for equipment in self.equipments:
            total_defense_power += equipment.get_defense_bonus()
        return total_defense_power

    def get_equipment(self, slot_name: str):
        for equipment in self.equipments:
            if equipment.slot == slot_name:
                return equipment
        return None

    def is_slot_available(self, slot_name: str):
        return self.get_equipment(slot_name) is None

    def equip_item(self, item: Equipable):
        if  not self.is_slot_available(item.slot):
            return False

        self.equipments.append(item)
        self.max_health += item.get_health_bonus()

        return True

    def unequip_item(self, item: Equipable):
        if item in self.equipments:
            self.equipments.remove(item)
            self.max_health -= item.get_health_bonus()
            self.health = min(self.health, self.max_health)

    def play_turn(self):
        return self.attack_target()

class Enemy(Entity):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int, dropable: list):
        super().__init__(name, health, power_attack, power_defense, is_ennemy=True)
        self.dropable = dropable

    def drop_loot(self, multiplier: float = 1.0) -> list:
        dropped_items = []
        for item in self.dropable:
            if item.roll_drop(multiplier):
                dropped_items.append(item)
        return dropped_items

    def play_turn(self):
        return self.attack_target()