from pokemon_game.damage_context import DamageContext
from pokemon_game.damage_strategy import DamageStrategy
from pokemon_game.terrain import Terrain
from pokemon_game.weather import Weather


class Battle:
    """Contexte du pattern Strategy : délègue le calcul des dégâts."""

    def __init__(
        self,
        damage_strategy: DamageStrategy,
        weather: Weather = Weather.CLEAR,
        terrain: Terrain = Terrain.NORMAL,
    ):
        self.damage_strategy = damage_strategy
        self.weather = weather
        self.terrain = terrain

    def calculate_damage(self, attacker, defender, attack) -> int:
        context = DamageContext(self.weather, self.terrain)
        return self.damage_strategy.calculate(attack, attacker, defender, context)

    def attack(self, attacker, defender, attack) -> int:
        damage = self.calculate_damage(attacker, defender, attack)
        hp_before = defender.hp
        defender.take_damage(damage)
        return hp_before - defender.hp