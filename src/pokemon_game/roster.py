from dataclasses import dataclass

from pokemon_game.attack import Attack
from pokemon_game.pokemon import Pokemon
from pokemon_game.pokemon_type import PokemonType


class UnknownPokemon(ValueError):
    """La clé demandée n'existe pas dans le roster."""


@dataclass(frozen=True)
class PokemonSpec:
    """Fiche descriptive d'un Pokémon : des données, pas un Pokémon en combat."""

    name: str
    pokemon_type: PokemonType
    max_hp: int
    attacks: tuple[tuple[str, int, PokemonType], ...]

    def create(self) -> Pokemon:
        """Fabrique un Pokémon neuf, avec tous ses PV."""
        return Pokemon(
            self.name,
            self.max_hp,
            self.pokemon_type,
            [Attack(name, damage, attack_type) for name, damage, attack_type in self.attacks],
        )


ROSTER: dict[str, PokemonSpec] = {
    "pikachu": PokemonSpec(
        "Pikachu", PokemonType.ELECTRIC, 95,
        (("Tonnerre", 20, PokemonType.ELECTRIC), ("Vive-Attaque", 15, PokemonType.NORMAL)),
    ),
    "salameche": PokemonSpec(
        "Salamèche", PokemonType.FIRE, 100,
        (("Flammèche", 20, PokemonType.FIRE), ("Griffe", 15, PokemonType.NORMAL)),
    ),
    "bulbizarre": PokemonSpec(
        "Bulbizarre", PokemonType.GRASS, 110,
        (("Fouet Lianes", 20, PokemonType.GRASS), ("Charge", 15, PokemonType.NORMAL)),
    ),
    "carapuce": PokemonSpec(
        "Carapuce", PokemonType.WATER, 105,
        (("Pistolet à O", 20, PokemonType.WATER), ("Charge", 15, PokemonType.NORMAL)),
    ),
}


def create_pokemon(key: str) -> Pokemon:
    """Crée un Pokémon neuf à partir de sa clé ("pikachu", "salameche"...)."""
    try:
        spec = ROSTER[key]
    except KeyError:
        raise UnknownPokemon(f"Pokémon inconnu : {key}") from None
    return spec.create()