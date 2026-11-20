import pytest

from pokemon_game.pokemon_type import PokemonType, type_multiplier
from pokemon_game.roster import ROSTER, UnknownPokemon, create_pokemon


FAMILIES = [
    ("bulbizarre", "herbizarre", "florizarre"),
    ("salameche", "reptincel", "dracaufeu"),
    ("carapuce", "carabaffe", "tortank"),
    ("pikachu", "raichu"),
]


def test_roster_contains_every_family():
    assert set(ROSTER) == {key for family in FAMILIES for key in family}


def test_roster_is_in_pokedex_order():
    numbers = [spec.dex for spec in ROSTER.values()]

    assert numbers == sorted(set(numbers))


@pytest.mark.parametrize("family", FAMILIES, ids=lambda family: family[0])
def test_each_evolution_is_stronger_than_the_previous_stage(family):
    for before, after in zip(family, family[1:]):
        previous, evolution = ROSTER[before], ROSTER[after]

        assert evolution.pokemon_type == previous.pokemon_type
        assert evolution.max_hp > previous.max_hp
        assert max(d for _, d, _ in evolution.attacks) > max(d for _, d, _ in previous.attacks)


@pytest.mark.parametrize(
    "key, pokemon_type",
    [
        ("pikachu", PokemonType.ELECTRIC),
        ("salameche", PokemonType.FIRE),
        ("bulbizarre", PokemonType.GRASS),
        ("carapuce", PokemonType.WATER),
        ("raichu", PokemonType.ELECTRIC),
        ("dracaufeu", PokemonType.FIRE),
        ("florizarre", PokemonType.GRASS),
        ("tortank", PokemonType.WATER),
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