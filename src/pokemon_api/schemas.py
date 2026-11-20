from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from pokemon_game.difficulty_selector import DIFFICULTIES
from pokemon_game.match import Match
from pokemon_game.roster import ROSTER, PokemonSpec
from pokemon_game.terrain import Terrain
from pokemon_game.weather import Weather

# ---------- Entrées : ce que le navigateur a le droit d'envoyer ----------

TrainerName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=20)]


class BattleCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trainer: TrainerName = "Sacha"
    pokemon: str
    opponent: str | None = None             # None : adversaire tiré au sort
    difficulty: str = "medium"
    weather: Weather = Weather.CLEAR
    terrain: Terrain = Terrain.NORMAL

    @field_validator("pokemon", "opponent")
    @classmethod
    def must_be_in_roster(cls, key: str | None) -> str | None:
        if key is not None and key not in ROSTER:
            raise ValueError(f"Pokémon inconnu. Choix possibles : {', '.join(ROSTER)}")
        return key

    @field_validator("difficulty")
    @classmethod
    def must_be_a_difficulty(cls, key: str) -> str:
        if key not in DIFFICULTIES:
            raise ValueError(f"Difficulté inconnue. Choix possibles : {', '.join(DIFFICULTIES)}")
        return key


class AttackRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    attack_index: int = Field(ge=0)


# ---------- Sorties : ce que le serveur promet de renvoyer ----------

class Option(BaseModel):
    key: str
    label: str

class Condition(Option):
    modifiers: dict[str, float]          # type d'attaque -> multiplicateur



class AttackOut(BaseModel):
    name: str
    damage: int
    type: str


class RosterEntry(BaseModel):
    key: str
    dex: int
    name: str
    type: str
    max_hp: int
    attacks: list[AttackOut]


class Options(BaseModel):
    pokemon: list[RosterEntry]
    difficulties: list[Option]
    weathers: list[Condition]
    terrains: list[Condition]


class PokemonOut(BaseModel):
    name: str
    type: str
    hp: int
    max_hp: int
    attacks: list[AttackOut]


class TrainerOut(BaseModel):
    name: str
    pokemon: PokemonOut
    potions: int


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)    # lit les attributs d'un Event

    kind: str
    side: str
    message: str
    damage: int
    heal: int
    hp: int | None
    effectiveness: float


class BattleOut(BaseModel):
    id: str
    status: Literal["in_progress", "won", "lost"]
    turn: int
    difficulty: str
    weather: Weather
    terrain: Terrain
    player: TrainerOut
    opponent: TrainerOut
    log: list[EventOut]


# ---------- Conversions domaine -> réponse ----------

def roster_entry(key: str, spec: PokemonSpec) -> RosterEntry:
    return RosterEntry(
        key=key,
        dex=spec.dex,
        name=spec.name,
        type=spec.pokemon_type.value,
        max_hp=spec.max_hp,
        attacks=[AttackOut(name=name, damage=damage, type=attack_type.value)
                 for name, damage, attack_type in spec.attacks],
    )


def trainer_out(trainer) -> TrainerOut:
    pokemon = trainer.pokemon
    return TrainerOut(
        name=trainer.name,
        potions=len(trainer.potions),
        pokemon=PokemonOut(
            name=pokemon.name,
            type=pokemon.type.value,
            hp=pokemon.hp,
            max_hp=pokemon.max_hp,
            attacks=[AttackOut(name=a.name, damage=a.damage, type=a.type.value)
                     for a in pokemon.attacks],
        ),
    )


def battle_out(battle_id: str, match: Match) -> BattleOut:
    return BattleOut(
        id=battle_id,
        status=match.status,
        turn=match.turn,
        difficulty=match.difficulty,
        weather=match.battle.weather,
        terrain=match.battle.terrain,
        player=trainer_out(match.player),
        opponent=trainer_out(match.computer),
        log=[EventOut.model_validate(event) for event in match.log],
    )