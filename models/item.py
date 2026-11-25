from typing import Dict

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

    def use(self, character):
        for stat, value in self.effect.items():
            if hasattr(character, stat):
                setattr(character, stat, getattr(character, stat) + value)