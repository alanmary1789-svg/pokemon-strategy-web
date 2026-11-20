import pytest

from pokemon_game.attack import Attack
from pokemon_game.battle import Battle
from pokemon_game.damage_calculator import DamageCalculator
from pokemon_game.damage_context import DamageContext
from pokemon_game.damage_strategy import DamageStrategy, SimpleDamageStrategy
from pokemon_game.pokemon import Pokemon
from pokemon_game.pokemon_type import PokemonType


def test_damage_strategy_cannot_be_instantiated():
    with pytest.raises(TypeError):
        DamageStrategy()


def test_damage_calculator_is_a_damage_strategy():
    assert isinstance(DamageCalculator(), DamageStrategy)


def test_simple_strategy_ignores_types_weather_and_terrain():
    ember = Attack("Ember", 20, PokemonType.FIRE)
    charmander = Pokemon("Charmander", 100, PokemonType.FIRE)
    bulbasaur = Pokemon("Bulbasaur", 100, PokemonType.GRASS)

    damage = SimpleDamageStrategy().calculate(
        ember, charmander, bulbasaur, DamageContext()
    )

    assert damage == 20


@pytest.mark.parametrize(
    "strategy, expected_hp",
    [
        (SimpleDamageStrategy(), 80),  # dégâts de base
        (DamageCalculator(), 60),      # feu super efficace contre plante
    ],
)
def test_battle_strategies_are_interchangeable(strategy, expected_hp):
    ember = Attack("Ember", 20, PokemonType.FIRE)
    charmander = Pokemon("Charmander", 100, PokemonType.FIRE)
    bulbasaur = Pokemon("Bulbasaur", 100, PokemonType.GRASS)

    Battle(strategy).attack(charmander, bulbasaur, ember)

    assert bulbasaur.hp == expected_hp


def test_damage_is_rounded_down_to_an_integer():
    spark = Attack("Spark", 15, PokemonType.ELECTRIC)
    pikachu = Pokemon("Pikachu", 100, PokemonType.ELECTRIC)
    bulbasaur = Pokemon("Bulbasaur", 100, PokemonType.GRASS)

    damage = DamageCalculator().calculate(
        spark, pikachu, bulbasaur, DamageContext()
    )

    assert damage == 7          # 15 x 0.5 = 7.5, arrondi à 7
    assert isinstance(damage, int)