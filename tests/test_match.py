import random

import pytest

from pokemon_game.match import IN_PROGRESS, LOST, WON, MatchError, MatchOver, start_match
from pokemon_game.roster import UnknownPokemon
from pokemon_game.weather import Weather


def make_match(**options):
    """Pikachu contre Carapuce, rival « moyen » (attaque la plus forte) : déterministe."""
    settings = {
        "trainer": "Sacha",
        "pokemon_key": "pikachu",
        "opponent_key": "carapuce",
        "difficulty": "medium",
    }
    return start_match(**{**settings, **options})


def test_new_match_starts_in_progress_with_full_hp():
    match = make_match()

    assert match.status == IN_PROGRESS
    assert match.turn == 1
    assert match.player.pokemon.hp == 95
    assert match.computer.pokemon.hp == 105
    assert len(match.player.potions) == 2
    assert match.log == []


def test_attack_hits_the_opponent_then_the_computer_replies():
    match = make_match()

    events = match.attack(0)                     # Tonnerre

    assert [event.kind for event in events] == ["attack", "attack"]
    assert events[0].side == "player"
    assert events[0].damage == 40                # électrique x2 contre eau
    assert "C'est super efficace !" in events[0].message
    assert events[1].side == "opponent"
    assert events[1].damage == 20                # Pistolet à O, neutre
    assert match.computer.pokemon.hp == 65
    assert match.player.pokemon.hp == 75
    assert match.turn == 2
    assert match.log == events


def test_unknown_attack_is_refused_and_changes_nothing():
    match = make_match()

    with pytest.raises(MatchError):
        match.attack(5)

    assert match.computer.pokemon.hp == 105
    assert match.player.pokemon.hp == 95
    assert match.turn == 1
    assert match.log == []


def test_potion_at_full_hp_is_refused_and_gives_no_free_turn():
    match = make_match()

    with pytest.raises(MatchError):
        match.use_potion()

    assert len(match.player.potions) == 2
    assert match.player.pokemon.hp == 95         # le rival n'a pas joué
    assert match.turn == 1


def test_potion_heals_then_the_computer_replies():
    match = make_match()
    match.attack(0)                              # Pikachu : 95 -> 75

    events = match.use_potion()

    assert events[0].kind == "potion"
    assert events[0].heal == 20                  # plafonné à 95 PV
    assert events[1].side == "opponent"
    assert match.player.pokemon.hp == 75         # 95 - 20
    assert len(match.player.potions) == 1


def test_match_is_won_and_the_computer_does_not_reply_after_ko():
    match = make_match()
    match.attack(0)                              # Carapuce : 105 -> 65
    match.attack(0)                              # 65 -> 25

    events = match.attack(0)                     # 25 -> 0

    assert [event.kind for event in events] == ["attack", "ko"]
    assert events[0].damage == 25                # dégâts réellement infligés
    assert match.status == WON
    assert match.player.pokemon.hp == 55         # seulement deux ripostes


def test_no_action_is_accepted_after_the_end():
    match = make_match()
    for _ in range(3):
        match.attack(0)

    with pytest.raises(MatchOver):
        match.attack(0)
    with pytest.raises(MatchOver):
        match.use_potion()


def test_match_is_lost_when_the_player_pokemon_is_ko():
    match = make_match(pokemon_key="bulbizarre", opponent_key="salameche", difficulty="hard")

    while match.status == IN_PROGRESS:
        match.attack(1)                          # Charge

    assert match.status == LOST
    assert match.log[-1].kind == "ko"
    assert match.log[-1].side == "player"


def test_weather_reaches_the_damage_strategy():
    match = make_match(pokemon_key="salameche", opponent_key="pikachu", weather=Weather.RAIN)

    events = match.attack(0)                     # Flammèche sous la pluie

    assert events[0].damage == 10


def test_random_opponent_is_never_the_player_pokemon():
    for seed in range(20):
        match = start_match("Sacha", "pikachu", rng=random.Random(seed))
        assert match.computer.pokemon.name != "Pikachu"


def test_unknown_pokemon_or_difficulty_is_refused():
    with pytest.raises(UnknownPokemon):
        start_match("Sacha", "mewtwo")
    with pytest.raises(ValueError):
        start_match("Sacha", "pikachu", difficulty="legend")