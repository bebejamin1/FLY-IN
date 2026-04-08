# FLY-IN

FLY-IN/
│
├── Makefile                  # Les commandes d'installation et de test (lint, run)
├── pyproject.toml            # Les dépendances (pydantic) et la config
├── README.md                 # Ta documentation
│
├── maps/                     # Ton dossier contenant les cartes
│   ├── easy/
│   │   └── level1.txt
│   └── hard/
│       └── maze.txt
│
├── main.py                   # 📍 LE POINT D'ENTRÉE (Le Chef d'Orchestre)
│   └── def main()            # Coordonne le Menu -> le Parser -> l'Algo -> l'Affichage
│
├── menu/                     # 📂 PACKAGE : Interface utilisateur initiale
│   ├── __init__.py
│   └── selector.py
│       └── class MapSelector:
│           ├── def __init__()
│           ├── def get_available_level()
│           ├── def display_file()
│           └── def prompt_user() -> Path
│
├── parsing/                  # 📂 PACKAGE : Lecture et validation des fichiers
│   ├── __init__.py
│   ├── models.py             # Les "Mots" de ton projet (Data Classes)
│   │   ├── class Zone(BaseModel):         # Définit x, y, type, capacité
│   │   ├── class Connection(BaseModel):   # Définit les liens
│   │   └── class MapData(BaseModel):      # Contient tout (hub, start, liste des zones)
│   │
│   └── map_parser.py         # L'usine qui fabrique les modèles
│       └── class MapParser:
│           ├── def __init__(filepath: Path)
│           ├── def parse() -> MapData
│           ├── def _extract_metadata(line) -> dict
│           ├── def _parse_drones(line)
│           ├── def _parse_zone(line)
│           └── def _parse_connection(line)
│
├── core/                     # 📂 PACKAGE : Le cerveau (Mouvement et Algo)
│   ├── __init__.py
│   ├── pathfinder.py         # L'algorithme de recherche
│   │   └── class Pathfinder:
│   │       ├── def __init__(map_data: MapData)
│   │       ├── def find_shortest_paths()  # Ton BFS / algorithme de graphe
│   │       └── def _is_valid_move()       # Vérifie si le chemin est libre
│   │
│   └── engine.py             # Le moteur de jeu (tour par tour)
│       └── class SimulationEngine:
│           ├── def __init__(map_data, paths)
│           ├── def run_simulation()       # La boucle while principale
│           ├── def move_drones()
│           └── def check_capacities()
│
└── visualize/                # 📂 PACKAGE : Les Yeux (Affichage de la simulation)
    ├── __init__.py
    └── renderer.py
        └── class TerminalRenderer:
            ├── def __init__()
            ├── def draw_map(map_data: MapData)
            ├── def update_drones(turn: int, moves: list)
            └── def display_results(score: int)