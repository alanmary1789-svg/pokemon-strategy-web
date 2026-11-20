import pytest

from pokemon_game.pokemon_type import PokemonType, type_multiplier
from pokemon_game.roster import ROSTER, UnknownPokemon, create_pokemon


def test_roster_contains_the_four_starters():
    assert set(ROSTER) == {"pikachu", "salameche", "bulbizarre", "carapuce"}


@pytest.mark.parametrize(
    "key, pokemon_type",
    [
        ("pikachu", PokemonType.ELECTRIC),
        ("salameche", PokemonType.FIRE),
        ("bulbizarre", PokemonType.GRASS),
        ("carapuce", PokemonType.WATER),
    ],
)
def test_each_pokemon_has_its_type_and_full_hp(key, pokemon_type):
    pokemon = create_pokemon(key)

    assert pokemon.type == pokemon_type
    assert pokemon.hp == pokemon.max_hp


@pytest.mark.parametrize("key", sorted(ROSTER))
def test_each_pokemon_has_an_attack_of_its_type_and_a_normal_attack(key):
    pokemon = create_pokemon(key)
    attack_types = {attack.type for attack in pokemon.attacks}

    assert pokemon.type in attack_types
    assert PokemonType.NORMAL in attack_types


def test_create_pokemon_returns_a_fresh_instance_each_time():
    first = create_pokemon("pikachu")
    first.take_damage(30)

    second = create_pokemon("pikachu")

    assert second is not first
    assert second.hp == second.max_hp


def test_unknown_pokemon_raises_a_clear_error():
    with pytest.raises(UnknownPokemon):
        create_pokemon("mewtwo")


@pytest.mark.parametrize(
    "defender_type",
    [PokemonType.FIRE, PokemonType.WATER, PokemonType.GRASS, PokemonType.ELECTRIC],
)
def test_normal_attacks_are_neutral_against_every_type(defender_type):
    assert type_multiplier(PokemonType.NORMAL, defender_type) == 1.0