import pytest

from pokemon_game.difficulty_selector import choose_difficulty
from pokemon_game.attack_strategy import (
    RandomAttackStrategy,
    StrongestAttackStrategy,
    EffectiveAttackStrategy,
)


@pytest.mark.parametrize(
    "choice, expected_strategy",
    [
        ("1", RandomAttackStrategy),
        ("2", StrongestAttackStrategy),
        ("3", EffectiveAttackStrategy),
    ]
)
def test_choose_difficulty_returns_correct_strategy(
    monkeypatch,
    choice,
    expected_strategy
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: choice
    )

    strategy = choose_difficulty()

    assert isinstance(strategy, expected_strategy)


def test_invalid_difficulty_asks_again(monkeypatch):
    inputs = iter(["abc", "5", "2"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    strategy = choose_difficulty()

    assert isinstance(strategy, StrongestAttackStrategy)

from pokemon_game.difficulty_selector import create_attack_strategy


@pytest.mark.parametrize(
    "difficulty, expected_strategy",
    [
        ("easy", RandomAttackStrategy),
        ("medium", StrongestAttackStrategy),
        ("hard", EffectiveAttackStrategy),
    ],
)
def test_create_attack_strategy_from_a_difficulty_key(difficulty, expected_strategy):
    assert isinstance(create_attack_strategy(difficulty), expected_strategy)


def test_unknown_difficulty_is_refused():
    with pytest.raises(ValueError):
        create_attack_strategy("legend")