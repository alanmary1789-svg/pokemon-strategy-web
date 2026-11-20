from abc import ABC, abstractmethod


class DamageStrategy(ABC):
    """Interface du pattern Strategy : transforme une attaque en dégâts."""

    @abstractmethod
    def calculate(self, attack, attacker, defender, context) -> int:
        """Renvoie les dégâts (entier) sans modifier les Pokémon."""


class SimpleDamageStrategy(DamageStrategy):
    """Dégâts de base de l'attaque, sans aucun modificateur."""

    def calculate(self, attack, attacker, defender, context) -> int:
        return attack.damage