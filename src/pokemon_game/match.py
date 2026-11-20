import random
from dataclasses import dataclass

from pokemon_game.battle import Battle
from pokemon_game.computer_player import ComputerPlayer
from pokemon_game.damage_calculator import DamageCalculator
from pokemon_game.difficulty_selector import create_attack_strategy
from pokemon_game.player import Player
from pokemon_game.pokemon_type import type_multiplier
from pokemon_game.potion import Potion
from pokemon_game.roster import ROSTER, create_pokemon
from pokemon_game.terrain import Terrain
from pokemon_game.weather import Weather

IN_PROGRESS = "in_progress"
WON = "won"
LOST = "lost"


class MatchError(Exception):
    """Action refusée par les règles (attaque inconnue, potion inutile...)."""


class MatchOver(MatchError):
    """Le combat est terminé : plus aucune action n'est possible."""


@dataclass(frozen=True)
class Event:
    """Ce qui s'est passé pendant un tour, prêt à être affiché par n'importe quelle interface."""

    kind: str                  # "attack" | "potion" | "ko"
    side: str                  # "player" | "opponent" : qui agit (ou qui tombe K.O.)
    message: str
    damage: int = 0
    heal: int = 0
    hp: int | None = None      # PV de la cible après l'action
    effectiveness: float = 1.0


class Match:
    """Un combat joueur contre ordinateur, piloté action par action, sans input() ni print()."""

    def __init__(self, player: Player, computer: ComputerPlayer, battle: Battle, difficulty: str | None = None):
        self.player = player
        self.computer = computer
        self.battle = battle
        self.difficulty = difficulty
        self.turn = 1
        self.log: list[Event] = []

    @property
    def status(self) -> str:
        if self.computer.pokemon.is_ko():
            return WON
        if self.player.pokemon.is_ko():
            return LOST
        return IN_PROGRESS

    def attack(self, attack_index: int) -> list[Event]:
        """Le joueur attaque, puis le rival riposte s'il est encore debout."""
        self._ensure_in_progress()
        attacks = self.player.pokemon.attacks
        if not 0 <= attack_index < len(attacks):
            raise MatchError("Cette attaque n'existe pas.")
        events = self._hit(self.player, self.computer, attacks[attack_index], side="player")
        return self._finish_turn(events)

    def use_potion(self) -> list[Event]:
        """Le joueur utilise sa première potion, puis le rival riposte."""
        self._ensure_in_progress()
        if not self.player.potions:
            raise MatchError("Aucune potion disponible.")
        potion = self.player.potions[0]
        pokemon = self.player.pokemon
        hp_before = pokemon.hp
        try:
            self.player.use_potion(potion)
        except ValueError as error:          # PV déjà au maximum
            raise MatchError(str(error)) from error
        healed = pokemon.hp - hp_before
        message = f"{self.player.name} utilise {potion.name} : {pokemon.name} récupère {healed} PV."
        events = [Event("potion", "player", message, heal=healed, hp=pokemon.hp)]
        return self._finish_turn(events)

    def _finish_turn(self, events: list[Event]) -> list[Event]:
        if self.status == IN_PROGRESS:
            attack = self.computer.choose_attack(self.player.pokemon, self.battle)
            events += self._hit(self.computer, self.player, attack, side="opponent")
        self.turn += 1
        self.log.extend(events)
        return events

    def _hit(self, attacker, defender, attack, side: str) -> list[Event]:
        damage = self.battle.attack(attacker.pokemon, defender.pokemon, attack)
        effectiveness = type_multiplier(attack.type, defender.pokemon.type)

        message = f"{attacker.pokemon.name} utilise {attack.name} !"
        if effectiveness > 1:
            message += " C'est super efficace !"
        elif effectiveness < 1:
            message += " Ce n'est pas très efficace…"
        message += f" {defender.pokemon.name} perd {damage} PV."

        events = [Event("attack", side, message, damage=damage,
                        hp=defender.pokemon.hp, effectiveness=effectiveness)]
        if defender.pokemon.is_ko():
            ko_side = "opponent" if side == "player" else "player"
            events.append(Event("ko", ko_side, f"{defender.pokemon.name} est K.O. !", hp=0))
        return events

    def _ensure_in_progress(self) -> None:
        if self.status != IN_PROGRESS:
            raise MatchOver("Le combat est terminé.")


def start_match(
    trainer: str,
    pokemon_key: str,
    opponent_key: str | None = None,
    difficulty: str = "medium",
    weather: Weather = Weather.CLEAR,
    terrain: Terrain = Terrain.NORMAL,
    rng: random.Random | None = None,
) -> Match:
    """Assemble un combat complet : c'est ici qu'on choisit les stratégies à brancher."""
    rng = rng or random.Random()
    player_pokemon = create_pokemon(pokemon_key)            # UnknownPokemon si clé inconnue
    if opponent_key is None:
        opponent_key = rng.choice([key for key in ROSTER if key != pokemon_key])

    player = Player(trainer, player_pokemon, [Potion("Potion", 30), Potion("Potion", 30)])
    computer = ComputerPlayer("Rival", create_pokemon(opponent_key), create_attack_strategy(difficulty))
    battle = Battle(DamageCalculator(), weather=weather, terrain=terrain)
    return Match(player, computer, battle, difficulty=difficulty)