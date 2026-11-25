from function.utils import clamp

class Entity:
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int, is_ennemy: bool = False):
        self.name = name
        self.health = health
        self.max_health = health
        self.power_attack = power_attack
        self.power_defense = power_defense
        self.is_ennemy = is_ennemy

    def set_health(self, health: int):
        health = max(health, 0)
        self.health = health

    def take_damage(self, other_character):
        power_attack = other_character.power_attack - self.power_defense
        power_attack = max(2, power_attack)

        new_health = self.health - power_attack
        self.set_health(new_health)

        return power_attack

        # TODO: Refaire l'affichage dans des fonctions séparés
        # print(f"{self.name} a subit {power_attack} de dégâts de la part de {other_character.name}")

        # if new_health < 1:
        #     print(f"{self.name} est mort !")

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
        """OVERWRITE THIS FUNCTION IN CHILD CLASS"""
        pass

class Character(Entity):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int):
        super().__init__(name, health, power_attack, power_defense, is_ennemy=False)


    def play_turn(self):
        pass

class Enemy(Entity):
    def __init__(self, name: str, health: int, power_attack: int, power_defense: int, dropable: list):
        super().__init__(name, health, power_attack, power_defense, is_ennemy=True)
        self.dropable = dropable
        self.allies_choose = None

    def play_turn(self):
        if not self.allies_choose:
            return None

        attack = self.take_damage(self.allies_choose)
        return attack

    # Pour chaque item dropapble, on va faire un lancé. Un ennemi peut dropper plusieurs items, mais pas forcément tous. On va donc faire un lancé pour chaque item. Si le lancé est réussi, on ajoute l'item à la liste des items dropés. On retourne ensuite cette liste.
    def drop_loot(self):
       # return self.dropable
       pass