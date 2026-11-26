from function.utils import clamp
from models.item import Equipable
from typing import List

class Entity:
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

    def take_damage(self, other_character):
        power_attack = other_character.get_attack_power() - self.get_defense_power()
        power_attack = max(2, power_attack)

        new_health = self.health - power_attack
        self.set_health(new_health)

        print(f"{self.name} a subit {power_attack} de dégâts de la part de {other_character.name} (PV restant : {self.health}/{self.max_health})")
        return power_attack

        # TODO: Refaire l'affichage dans des fonctions séparés

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

    def play_turn(self):
        if not self.target:
            return None

        attack = self.target.take_damage(self)
        return attack

class Character(Entity):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int):
        super().__init__(name, health, power_attack, power_defense, is_ennemy=False)
        self.equipments: List[Equipable] = []

    @classmethod
    def create_character(cls, info_character: dict):
        if not Entity.is_valid_values_for_character(info_character):
            return None

        return Character(
            info_character["name"],
            info_character["health"],
            info_character["power_attack"],
            info_character["power_defense"],
        )

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
            print(f"Le slot {item.slot} est déjà occupé par un autre équipement.")
            return False

        self.equipments.append(item)
        self.max_health += item.get_health_bonus()

    def unequip_item(self, item: Equipable):
        if item in self.equipments:
            self.equipments.remove(item)
            self.max_health -= item.get_health_bonus()
            self.health = min(self.health, self.max_health)

class Enemy(Entity):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int, dropable: list):
        super().__init__(name, health, power_attack, power_defense, is_ennemy=True)
        self.dropable = dropable

    def drop_loot(self) -> list:
        dropped_items = []
        for item in self.dropable:
            if item.roll_drop():
                dropped_items.append(item)
        return dropped_items