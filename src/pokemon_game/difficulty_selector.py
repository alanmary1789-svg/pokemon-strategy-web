from pokemon_game.attack_strategy import (
    AttackStrategy,
    EffectiveAttackStrategy,
    RandomAttackStrategy,
    StrongestAttackStrategy,
)

# Une seule table pour le terminal ET le site : clé -> (libellé, stratégie)
DIFFICULTIES = {
    "easy": ("Facile", RandomAttackStrategy),
    "medium": ("Moyen", StrongestAttackStrategy),
    "hard": ("Difficile", EffectiveAttackStrategy),
}


def create_attack_strategy(difficulty: str) -> AttackStrategy:
    """Instancie la stratégie d'attaque correspondant à une difficulté."""
    if difficulty not in DIFFICULTIES:
        raise ValueError(f"Difficulté inconnue : {difficulty}")
    _, strategy_class = DIFFICULTIES[difficulty]
    return strategy_class()


def choose_difficulty():
    choices = dict(zip(["1", "2", "3"], DIFFICULTIES))   # "1" -> "easy"...

    print("=== Pokémon Battle ===")
    print()
    print("Choisissez la difficulté :")
    for number, key in choices.items():
        print(f"{number}. {DIFFICULTIES[key][0]}")

    while True:
        choice = input("> ")

        if choice in choices:
            key = choices[choice]
            print(f"Difficulté sélectionnée : {DIFFICULTIES[key][0]}")
            return create_attack_strategy(key)

        print("Choix invalide. Veuillez entrer 1, 2 ou 3.")