# Arène des types — Pokémon Strategy

Jeu de combat Pokémon au tour par tour, construit en TDD autour du pattern Strategy :

- `Battle` délègue le calcul des dégâts à une `DamageStrategy` (simple, ou type × météo × terrain) ;
- `ComputerPlayer` délègue le choix de son attaque à une `AttackStrategy` (facile : au hasard, moyen : la plus forte, difficile : la plus efficace).

Le même moteur sert un jeu en terminal (`main.py`) et un site web : une API FastAPI et une interface React.

## Prérequis

- Python 3.11 ou plus récent
- Node.js 20 ou plus récent (pour le frontend)

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"          # guillemets obligatoires sous zsh

cd frontend
npm ci
cd ..
```

## Lancer le site (une seule commande après le build)

```bash
cd frontend && npm run build && cd ..
uvicorn pokemon_api.app:create_app --factory --port 8000
```

Ouvrir http://localhost:8000. La documentation de l'API est sur http://localhost:8000/docs.

## Développer (rechargement à chaud)

Deux terminaux :

```bash
# Terminal 1 — l'API
uvicorn pokemon_api.app:create_app --factory --reload --port 8000

# Terminal 2 — l'interface (Vite relaie /api vers le port 8000)
cd frontend
npm run dev
```

Ouvrir http://localhost:5173.

## Tests

```bash
python -m pytest -q
```

## Jouer dans le terminal

```bash
python main.py
```

## Organisation

| Dossier | Rôle |
| --- | --- |
| `src/pokemon_game/` | Domaine : Pokémon, attaques, types, météo, terrain, stratégies, moteur `Match` |
| `src/pokemon_api/` | API FastAPI : schémas Pydantic, stockage des combats, routes |
| `frontend/` | Interface React (Vite) |
| `tests/` | Tests pytest du domaine et de l'API |

## API

| Requête | Effet |
| --- | --- |
| `GET /api/options` | Roster, difficultés, météos et terrains avec leurs multiplicateurs |
| `POST /api/battles` | Crée un combat (`trainer`, `pokemon`, `opponent`, `difficulty`, `weather`, `terrain`) |
| `GET /api/battles/{id}` | État d'un combat |
| `POST /api/battles/{id}/attack` | Le joueur attaque (`attack_index`), le rival riposte |
| `POST /api/battles/{id}/potion` | Le joueur utilise une potion, le rival riposte |

Codes d'erreur : `422` requête mal formée, `400` action interdite par les règles, `409` combat terminé, `404` combat inconnu.

## Limites connues

- Les combats en cours sont gardés en mémoire : ils sont perdus au redémarrage du serveur.
- Pas de comptes : l'identifiant aléatoire d'un combat est la seule clé pour y jouer.
- Les Pokémon sont représentés par l'emblème de leur type, pas par des illustrations officielles.


## Crédits

Les sprites des Pokémon sont © Nintendo / Creatures Inc. / GAME FREAK Inc. Ils sont chargés depuis [PokeAPI/sprites](https://github.com/PokeAPI/sprites) et ne sont pas distribués avec ce dépôt. Sans connexion internet, l'arène affiche l'emblème du type à la place.