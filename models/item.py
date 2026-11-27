from abc import abstractmethod
from typing import Dict
from database.function import get_rarities
from random import random

class Item:
    def __init__(self, name: str, item_type: str, rarity: str, effect: Dict[str, int], description: str = "", drop_rate: float = 0.0):
        self.name = name
        self.description = description
        self.item_type = item_type
        self.rarity = rarity
        self.effect = effect
        self.drop_rate = drop_rate

    @property
    @abstractmethod
    def consumable(self) -> bool:
        pass

    def __dict__(self):
        return {
            "name": self.name,
            "item_type": self.item_type,
            "rarity": self.rarity,
            "effect": self.effect,
            "consumable": self.consumable
        }
    def roll_drop(self, multiplier: float = 1.0) -> bool:
        """Determine if the item is dropped based on its rarity."""
        chance = min(1, self.drop_rate * multiplier)
        return random() < chance

    @staticmethod
    def create(name: str, item_type: str, rarity: str, effect: Dict[str, int], consumable: bool, description: str = "", drop_rate: float = 0.0) -> "Item":
        item_class = Consumable if consumable else Equipable
        return item_class(name, item_type, rarity, effect, description, drop_rate)

    @staticmethod
    def from_dict(info_item: dict, rarities: Dict[str, float] = None):
        if not info_item or not info_item.get("name"):
            return None

        effect = info_item.get("effect", {})
        rarity = info_item.get("rarity", "common")

        return Item.create(
            info_item["name"],
            info_item.get("item_type", "consumable"),
            rarity,
            effect,
            info_item.get("consumable", False),
            info_item.get("description", ""),
            (rarities.get(rarity, 0.0) if rarities else 0.0)
        )

class Equipable(Item):
    def __init__(self, name: str, item_type: str, rarity: str, effect: Dict[str, int], description: str = "", drop_rate: float = 0.0):
        super().__init__(name, item_type, rarity, effect, description, drop_rate)
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
    def __init__(self, name: str, item_type: str, rarity: str, effect: Dict[str, int], description: str = "", drop_rate: float = 0.0):
        super().__init__(name, item_type, rarity, effect, description, drop_rate)

    @property
    def consumable(self) -> bool:
        return True

    def use(self, character):
        for stat, value in self.effect.items():
            if stat == "health":
                character.heal(value)
            elif hasattr(character, stat):
                setattr(character, stat, getattr(character, stat) + value)