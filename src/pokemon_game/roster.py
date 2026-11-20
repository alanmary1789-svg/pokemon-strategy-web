from dataclasses import dataclass

from pokemon_game.attack import Attack
from pokemon_game.pokemon import Pokemon
from pokemon_game.pokemon_type import PokemonType


class UnknownPokemon(ValueError):
    """La clé demandée n'existe pas dans le roster."""


@dataclass(frozen=True)
class PokemonSpec:
    """Fiche descriptive d'un Pokémon : des données, pas un Pokémon en combat."""

    dex: int                     # numéro du Pokédex national
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


# Dans l'ordre du Pokédex national. Un seul type par Pokémon : le moteur ne gère pas les doubles types.
ROSTER: dict[str, PokemonSpec] = {
    "bulbizarre": PokemonSpec(
        1, "Bulbizarre", PokemonType.GRASS, 110,
        (("Fouet Lianes", 20, PokemonType.GRASS), ("Charge", 15, PokemonType.NORMAL)),
    ),
    "herbizarre": PokemonSpec(
        2, "Herbizarre", PokemonType.GRASS, 135,
        (("Tranch'Herbe", 25, PokemonType.GRASS), ("Bélier", 18, PokemonType.NORMAL)),
    ),
    "florizarre": PokemonSpec(
        3, "Florizarre", PokemonType.GRASS, 160,
        (("Lance-Soleil", 30, PokemonType.GRASS), ("Damoclès", 20, PokemonType.NORMAL)),
    ),
    "salameche": PokemonSpec(
        4, "Salamèche", PokemonType.FIRE, 100,
        (("Flammèche", 20, PokemonType.FIRE), ("Griffe", 15, PokemonType.NORMAL)),
    ),
    "reptincel": PokemonSpec(
        5, "Reptincel", PokemonType.FIRE, 125,
        (("Lance-Flammes", 25, PokemonType.FIRE), ("Coupe", 18, PokemonType.NORMAL)),
    ),
    "dracaufeu": PokemonSpec(
        6, "Dracaufeu", PokemonType.FIRE, 150,
        (("Déflagration", 30, PokemonType.FIRE), ("Tranche", 20, PokemonType.NORMAL)),
    ),
    "carapuce": PokemonSpec(
        7, "Carapuce", PokemonType.WATER, 105,
        (("Pistolet à O", 20, PokemonType.WATER), ("Charge", 15, PokemonType.NORMAL)),
    ),
    "carabaffe": PokemonSpec(
        8, "Carabaffe", PokemonType.WATER, 130,
        (("Hydroqueue", 25, PokemonType.WATER), ("Morsure", 18, PokemonType.NORMAL)),
    ),
    "tortank": PokemonSpec(
        9, "Tortank", PokemonType.WATER, 155,
        (("Hydrocanon", 30, PokemonType.WATER), ("Coud'Krâne", 20, PokemonType.NORMAL)),
    ),
    "pikachu": PokemonSpec(
        25, "Pikachu", PokemonType.ELECTRIC, 95,
        (("Tonnerre", 20, PokemonType.ELECTRIC), ("Vive-Attaque", 15, PokemonType.NORMAL)),
    ),
    "raichu": PokemonSpec(
        26, "Raichu", PokemonType.ELECTRIC, 130,
        (("Fatal-Foudre", 30, PokemonType.ELECTRIC), ("Plaquage", 20, PokemonType.NORMAL)),
    ),
}


def create_pokemon(key: str) -> Pokemon:
    """Crée un Pokémon neuf à partir de sa clé ("pikachu", "salameche"...)."""
    try:
        spec = ROSTER[key]
    except KeyError:
        raise UnknownPokemon(f"Pokémon inconnu : {key}") from None
    return spec.create()