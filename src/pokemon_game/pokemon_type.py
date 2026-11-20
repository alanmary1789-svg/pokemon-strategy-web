from enum import Enum 

class PokemonType(Enum):
    FIRE = "fire"
    WATER = "water"
    GRASS = "grass"
    ELECTRIC = "electric"




TYPE_EFFECTIVENESS = {
    PokemonType.FIRE: {
        PokemonType.WATER: 0.5,
        PokemonType.GRASS: 2.0,
    },
    PokemonType.WATER: {
        PokemonType.FIRE: 2.0,
        PokemonType.WATER: 0.5,
        PokemonType.GRASS: 0.5,
    },
    PokemonType.GRASS: {
        PokemonType.FIRE: 0.5,
        PokemonType.WATER: 2.0,
        PokemonType.GRASS: 0.5,
    },
    PokemonType.ELECTRIC: {
        PokemonType.WATER: 2.0,
        PokemonType.GRASS: 0.5,
        PokemonType.ELECTRIC: 0.5,
    },
}

def type_multiplier(attack_type: PokemonType, defender_type: PokemonType) -> float:
    """Coefficient d'efficacité d'un type d'attaque contre le type du défenseur."""
    return TYPE_EFFECTIVENESS.get(attack_type, {}).get(defender_type, 1.0)