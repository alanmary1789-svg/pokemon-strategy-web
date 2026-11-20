import math

from pokemon_game.damage_strategy import DamageStrategy
from pokemon_game.pokemon_type import type_multiplier
from pokemon_game.terrain import TERRAIN_EFFECTIVENESS
from pokemon_game.weather import WEATHER_EFFECTIVENESS


class DamageCalculator(DamageStrategy):
    """Stratégie complète : type x météo x terrain, arrondie à l'entier inférieur."""

    def calculate(self, attack, attacker, defender, context) -> int:
        multiplier = (
            type_multiplier(attack.type, defender.type)
            * WEATHER_EFFECTIVENESS[context.weather].get(attack.type, 1)
            * TERRAIN_EFFECTIVENESS[context.terrain].get(attack.type, 1)
        )
        return math.floor(attack.damage * multiplier)