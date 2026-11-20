from pokemon_game.pokemon import Pokemon
from pokemon_game.attack import Attack 
from pokemon_game.pokemon_type import PokemonType, TYPE_EFFECTIVENESS

def test_attack_has_name_and_damage_and_type():
    attack = Attack("Foudre", 20, PokemonType.ELECTRIC)

    assert attack.name == "Foudre"
    assert attack.damage == 20
    assert attack.type == PokemonType.ELECTRIC

