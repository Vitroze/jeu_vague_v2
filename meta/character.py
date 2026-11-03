from dataclasses import dataclass

"""

"""

@dataclass
class Character():
    name: str
    health: int
    power_attack: int
    power_defense: int
    is_ennemy: bool = False

    def set_health(self, health: int):
        health = max(health, 0)

        self.health = health

    def take_damage(self, other_character):
        power_attack = other_character.power_attack - self.power_defense
        power_attack = max(2, power_attack)

        self.set_health(self.health - power_attack)

    def is_alive(self):
        return self.health > 0

    def is_death(self):
        return self.health <= 0

def is_valid_values_for_character(dict_character: dict)->bool:
    return dict_character.get("name") and dict_character.get("health") and dict_character.get("power_attack") and dict_character.get("power_defense")

def create_character(info_character:dict) ->Character|None:
    if not is_valid_values_for_character(info_character):
        return None

    return Character(
        info_character["name"],
        info_character["health"],
        info_character["power_attack"],
        info_character["power_defense"],
        info_character.get("is_ennemy"),
    )