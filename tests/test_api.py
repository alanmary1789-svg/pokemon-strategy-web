import pytest
from fastapi.testclient import TestClient

from pokemon_api.app import create_app


@pytest.fixture
def client():
    app = create_app(static_dir=None)          # l'API seule, sans le site
    with TestClient(app) as client:
        yield client


def new_battle(client, **overrides):
    """Pikachu contre Carapuce, rival moyen : un combat déterministe."""
    body = {
        "trainer": "Sacha",
        "pokemon": "pikachu",
        "opponent": "carapuce",
        "difficulty": "medium",
        **overrides,
    }
    response = client.post("/api/battles", json=body)
    assert response.status_code == 201, response.text
    return response.json()


def test_options_list_the_roster_and_the_choices(client):
    response = client.get("/api/options")

    assert response.status_code == 200
    data = response.json()
    assert [p["key"] for p in data["pokemon"]] == ["pikachu", "salameche", "bulbizarre", "carapuce"]
    assert data["pokemon"][0] == {
        "key": "pikachu",
        "name": "Pikachu",
        "type": "electric",
        "max_hp": 95,
        "attacks": [
            {"name": "Tonnerre", "damage": 20, "type": "electric"},
            {"name": "Vive-Attaque", "damage": 15, "type": "normal"},
        ],
    }
    assert data["difficulties"][0] == {"key": "easy", "label": "Facile"}
    assert {w["key"] for w in data["weathers"]} == {"clear", "rain", "sun"}
    assert {t["key"] for t in data["terrains"]} == {"normal", "grassy", "electric"}


def test_create_battle_returns_the_initial_state(client):
    battle = new_battle(client)

    assert battle["status"] == "in_progress"
    assert battle["turn"] == 1
    assert battle["player"]["name"] == "Sacha"
    assert battle["player"]["pokemon"]["hp"] == 95
    assert battle["player"]["potions"] == 2
    assert battle["opponent"]["pokemon"]["name"] == "Carapuce"
    assert battle["weather"] == "clear"
    assert battle["log"] == []
    assert client.get(f"/api/battles/{battle['id']}").json() == battle


@pytest.mark.parametrize(
    "body",
    [
        {},                                             # pokemon manquant
        {"pokemon": "mewtwo"},                          # hors roster
        {"pokemon": "pikachu", "opponent": "mewtwo"},
        {"pokemon": "pikachu", "difficulty": "legend"},
        {"pokemon": "pikachu", "weather": "snow"},
        {"pokemon": "pikachu", "trainer": "   "},
        {"pokemon": "pikachu", "hp": 999},              # champ inconnu
    ],
)
def test_invalid_battle_settings_are_rejected(client, body):
    response = client.post("/api/battles", json=body)

    assert response.status_code == 422


def test_attack_returns_the_new_state_with_the_turn_events(client):
    battle = new_battle(client)

    response = client.post(f"/api/battles/{battle['id']}/attack", json={"attack_index": 0})

    assert response.status_code == 200
    state = response.json()
    assert state["opponent"]["pokemon"]["hp"] == 65
    assert state["player"]["pokemon"]["hp"] == 75
    assert state["turn"] == 2
    assert [event["side"] for event in state["log"]] == ["player", "opponent"]
    assert state["log"][0]["effectiveness"] == 2.0
    assert state["log"][0]["message"].startswith("Pikachu utilise Tonnerre !")


def test_unknown_attack_is_a_400_and_changes_nothing(client):
    battle = new_battle(client)

    response = client.post(f"/api/battles/{battle['id']}/attack", json={"attack_index": 7})

    assert response.status_code == 400
    assert response.json() == {"detail": "Cette attaque n'existe pas."}
    assert client.get(f"/api/battles/{battle['id']}").json() == battle


@pytest.mark.parametrize("body", [{"attack_index": "zero"}, {"attack_index": -1}, {}])
def test_attack_body_is_validated(client, body):
    battle = new_battle(client)

    response = client.post(f"/api/battles/{battle['id']}/attack", json=body)

    assert response.status_code == 422


def test_potion_at_full_hp_is_a_400_and_keeps_the_potion(client):
    battle = new_battle(client)

    response = client.post(f"/api/battles/{battle['id']}/potion")

    assert response.status_code == 400
    assert client.get(f"/api/battles/{battle['id']}").json()["player"]["potions"] == 2


def test_potion_after_damage_heals_and_is_consumed(client):
    battle = new_battle(client)
    client.post(f"/api/battles/{battle['id']}/attack", json={"attack_index": 0})

    state = client.post(f"/api/battles/{battle['id']}/potion").json()

    assert state["player"]["potions"] == 1
    assert state["log"][2]["kind"] == "potion"
    assert state["log"][2]["heal"] == 20


def test_finished_battle_refuses_actions_with_a_409(client):
    battle = new_battle(client)
    for _ in range(3):
        state = client.post(f"/api/battles/{battle['id']}/attack", json={"attack_index": 0}).json()

    assert state["status"] == "won"
    assert state["log"][-1]["kind"] == "ko"
    response = client.post(f"/api/battles/{battle['id']}/attack", json={"attack_index": 0})
    assert response.status_code == 409


def test_unknown_battle_is_a_404(client):
    assert client.get("/api/battles/inconnu").status_code == 404
    assert client.post("/api/battles/inconnu/attack", json={"attack_index": 0}).status_code == 404
    assert client.post("/api/battles/inconnu/potion").status_code == 404


def test_each_battle_is_independent(client):
    first = new_battle(client)
    second = new_battle(client)

    client.post(f"/api/battles/{first['id']}/attack", json={"attack_index": 0})

    assert first["id"] != second["id"]
    assert client.get(f"/api/battles/{second['id']}").json() == second

def test_options_expose_weather_and_terrain_modifiers(client):
    data = client.get("/api/options").json()

    weathers = {w["key"]: w["modifiers"] for w in data["weathers"]}
    terrains = {t["key"]: t["modifiers"] for t in data["terrains"]}
    assert weathers["rain"] == {"fire": 0.5, "water": 1.5}
    assert weathers["clear"] == {}
    assert terrains["grassy"] == {"grass": 1.5}