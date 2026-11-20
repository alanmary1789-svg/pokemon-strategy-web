from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from pokemon_game.difficulty_selector import DIFFICULTIES
from pokemon_game.match import Match, MatchError, MatchOver, start_match
from pokemon_game.roster import ROSTER
from pokemon_game.terrain import TERRAIN_EFFECTIVENESS, TERRAIN_LABELS
from pokemon_game.weather import WEATHER_EFFECTIVENESS, WEATHER_LABELS

from .schemas import (
    AttackRequest,
    BattleCreate,
    BattleOut,
    Condition,
    Option,
    Options,
    battle_out,
    roster_entry,
)
from .store import BattleStore

# src/pokemon_api/app.py -> racine du projet -> frontend/dist (créé par « npm run build »)
FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"

def modifiers_of(table: dict) -> dict[str, float]:
    """{PokemonType.FIRE: 0.5} -> {"fire": 0.5} : des clés JSON lisibles par le front."""
    return {pokemon_type.value: multiplier for pokemon_type, multiplier in table.items()}


def create_app(static_dir: Path | None = FRONTEND_DIST) -> FastAPI:
    app = FastAPI(title="Pokémon Strategy API", version="1.0")
    store = BattleStore()

    # ----- Erreurs du domaine -> codes HTTP -----
    @app.exception_handler(MatchOver)
    async def match_over(request: Request, exc: MatchOver):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(MatchError)
    async def match_error(request: Request, exc: MatchError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    # ----- Dépendance : retrouver le combat ou répondre 404 -----
    def get_match(battle_id: str) -> Match:
        match = store.get(battle_id)
        if match is None:
            raise HTTPException(status_code=404, detail="Combat introuvable.")
        return match

    CurrentMatch = Annotated[Match, Depends(get_match)]

    # ----- Routes -----
    @app.get("/api/options", response_model=Options)
    def read_options():
        return Options(
            pokemon=[roster_entry(key, spec) for key, spec in ROSTER.items()],
            difficulties=[Option(key=key, label=label) for key, (label, _) in DIFFICULTIES.items()],
            weathers=[
                Condition(key=w.value, label=label, modifiers=modifiers_of(WEATHER_EFFECTIVENESS[w]))
                for w, label in WEATHER_LABELS.items()
            ],
            terrains=[
                Condition(key=t.value, label=label, modifiers=modifiers_of(TERRAIN_EFFECTIVENESS[t]))
                for t, label in TERRAIN_LABELS.items()
            ],
        )

    @app.post("/api/battles", response_model=BattleOut, status_code=201)
    def create_battle(settings: BattleCreate):
        match = start_match(
            trainer=settings.trainer,
            pokemon_key=settings.pokemon,
            opponent_key=settings.opponent,
            difficulty=settings.difficulty,
            weather=settings.weather,
            terrain=settings.terrain,
        )
        return battle_out(store.add(match), match)

    @app.get("/api/battles/{battle_id}", response_model=BattleOut)
    def read_battle(battle_id: str, match: CurrentMatch):
        return battle_out(battle_id, match)

    @app.post("/api/battles/{battle_id}/attack", response_model=BattleOut)
    def attack(battle_id: str, action: AttackRequest, match: CurrentMatch):
        match.attack(action.attack_index)
        return battle_out(battle_id, match)

    @app.post("/api/battles/{battle_id}/potion", response_model=BattleOut)
    def use_potion(battle_id: str, match: CurrentMatch):
        match.use_potion()
        return battle_out(battle_id, match)

    # ----- Le site (étape 6) : monté EN DERNIER pour ne pas masquer /api -----
    if static_dir is not None and static_dir.is_dir():
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="site")

    return app