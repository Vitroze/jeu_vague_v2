from abc import ABC, abstractmethod
from function.utils import clamp
from models.item import Consumable, Equipable
from models.affichage import Affichage
from models.vue import VueTourJoueur, VueChoixCible, VueSelectionObjet
from typing import List

class Entity(ABC):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int, is_ennemy: bool = False, max_health: int = None):
        self.name = name
        self.health = health
        self.max_health = health if max_health is None else max_health
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

    def attack(self, target: "Entity"):
        power_attack = self.get_attack_power() - target.get_defense_power()
        power_attack = max(2, power_attack)

        return target.take_damage(power_attack)

    def is_alive(self):
        return self.health >= 1

    def is_death(self):
        return self.health < 1

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

    def projected_attack(self, target: "Entity"):
        power_attack = self.get_attack_power() - target.get_defense_power()
        power_attack = max(2, power_attack)
        return power_attack

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

    def __str__(self):
        if isinstance(self, Character) and self.equipments:
            return f"{self.name} ; {', '.join([e.name for e in self.equipments])} (HP: {self.health}/{self.max_health}, ATK: {self.get_attack_power()}, DEF: {self.get_defense_power()})"
        return f"{self.name} (HP: {self.health}/{self.max_health}, ATK: {self.get_attack_power()}, DEF: {self.get_defense_power()})"

class Character(Entity):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int, max_health: int = None, equipment: List[Equipable] = None):
        super().__init__(name, health, power_attack, power_defense, is_ennemy=False, max_health=max_health)
        self.equipments = equipment if equipment is not None else []

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
        if not self.is_slot_available(item.slot):
            return False

        self.equipments.append(item)
        self.max_health += item.get_health_bonus()

        return True

    def unequip_item(self, item: Equipable):
        if item in self.equipments:
            self.equipments.remove(item)
            self.max_health -= item.get_health_bonus()
            self.health = min(self.health, self.max_health)

    def choose_cible(self, ennemies: List):
        if not ennemies:
            return None

        choice = Affichage.display_vue(VueChoixCible([], self, ennemies), len(ennemies))
        cible = ennemies[choice]
        return cible

    def attack_target(self, ennemies: List):
        target = self.choose_cible(ennemies)
        if not target:
            return None

        self.target = target
        amount = self.projected_attack(target)
        attack = target.take_damage(amount)
        return attack

    def get_choice_item(self, inventory, teams):
        if not inventory:
            return None

        choice = Affichage.display_vue(VueSelectionObjet(self, inventory), len(inventory))
        item = inventory[choice]
        return item

    def use_item(self, vague):
        inventory = vague.player.inventory
        allies = vague.player.get_team_alive()
        if not inventory:
            Affichage.show_error("Aucun objet disponible pour utilisation.")
            return self.play_turn(vague)

        item = self.get_choice_item(inventory, allies)

        if item in self.equipments and isinstance(item, Equipable):
            Affichage.show_error(f"{self.name} a déjà équipé {item.name}.")
            return self.play_turn(vague)
        elif not item in self.equipments and isinstance(item, Equipable):
            passed = self.equip_item(item)
            if not passed:
                Affichage.show_error(f"{self.name} ne peut pas équiper {item.name} car le slot est déjà occupé.")
                return self.play_turn(vague)

            inventory.remove(item)
            return f"{self.name} a équipé {item.name}."
        elif isinstance(item, Consumable):
            item.use(self)
            inventory.remove(item)
            return f"{self.name} a utilisé {item.name}."

    def unequip_item_menu(self, vague):
        if not self.equipments or len(self.equipments) == 0:
            Affichage.show_error(f"{self.name} n'a aucun objet équipé.")
            return self.play_turn(vague)

        choice = Affichage.display_vue(VueSelectionObjet(self, self.equipments, title=f"Choisir un objet à déséquiper pour {self.name}"), len(self.equipments))
        item = self.equipments[choice]

        self.unequip_item(item)
        return f"{self.name} a déséquipé {item.name}."

    def play_turn(self, vague) -> str:
        player = vague.player
        if not player:
            return 0

        ennemies = [ennemy for ennemy in vague.ennemies if ennemy.is_alive()]
        if not ennemies:
            return 0

        choice = Affichage.display_vue(VueTourJoueur(player.get_team_alive(), self, ennemies), 4)
        if choice == 0:
            damage = self.attack_target(vague.ennemies)
            return f"{self.name} attaque {self.target.name} et inflige {damage} degats !" if damage else f"{self.name} attaque mais rate sa cible !"
        elif choice == 1:
            return self.use_item(vague)
        elif choice == 2:
            return self.unequip_item_menu(vague)

        return f"{self.name} ne fait rien ce tour-ci."
        #return self.attack_target()

class Enemy(Entity):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int, dropable: list, max_health: int = None):
        super().__init__(name, health, power_attack, power_defense, is_ennemy=True, max_health=max_health)
        self.dropable = dropable

    def drop_loot(self, multiplier: float = 1.0) -> list:
        dropped_items = []
        for item in self.dropable:
            if item.roll_drop(multiplier):
                dropped_items.append(item)
        return dropped_items

    def attack_target(self):
        target = self.target
        if not target:
            return None

        amount = self.projected_attack(target)
        attack = target.take_damage(amount)
        return attack

    def play_turn(self) -> str:
        if not self.target or not self.target.is_alive():
            return 0

        damage = self.attack_target()
        return f"{self.name} attaque {self.target.name} et inflige {damage} degats !" if damage else f"{self.name} attaque mais rate sa cible !"