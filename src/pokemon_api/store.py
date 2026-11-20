import secrets

from pokemon_game.match import Match


class BattleStore:
    """Combats en cours, gardés dans la mémoire du processus (perdus au redémarrage)."""

    def __init__(self):
        self._matches: dict[str, Match] = {}

    def add(self, match: Match) -> str:
        battle_id = secrets.token_urlsafe(8)     # identifiant impossible à deviner
        self._matches[battle_id] = match
        return battle_id

    def get(self, battle_id: str) -> Match | None:
        return self._matches.get(battle_id)