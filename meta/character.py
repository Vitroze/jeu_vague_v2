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