from abc import abstractmethod
from typing import Dict
from database.function import get_rarities
from random import random

class Item:
    def __init__(self, name: str, item_type: str, rarity: str, effect: Dict[str, int], consumable: bool):
        self.name = name
        self.item_type = item_type
        self.rarity = rarity
        self.effect = effect
        self.consumable = consumable

    def __dict__(self):
        return {
            "name": self.name,
            "item_type": self.item_type,
            "rarity": self.rarity,
            "effect": self.effect,
            "consumable": self.consumable
        }

    def roll_drop(self) -> bool:
        """Determine if the item is dropped based on its rarity."""
        drop_chances = get_rarities()
        chance = drop_chances.get(self.rarity, 0)
        return random() < chance


class Equipable(Item):
    def __init__(self, name: str, item_type: str, rarity: str, effect: Dict[str, int], consumable: bool):
        super().__init__(name, item_type, rarity, effect, consumable)
        self.slot = item_type

    @property
    def consumable(self) -> bool:
        return False

    def get_attack_bonus(self) -> int:
        return self.effect.get("power_attack", 0)

    def get_defense_bonus(self) -> int:
        return self.effect.get("power_defense", 0)

    def get_health_bonus(self) -> int:
        return self.effect.get("health", 0)


class Consumable(Item):
    @property
    def consumable(self) -> bool:
        return True

    def use(self, character):
        for stat, value in self.effect.items():
            if stat == "health":
                character.heal(value)
            elif hasattr(character, stat):
                setattr(character, stat, getattr(character, stat) + value)