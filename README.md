*This project has been created as part of the 42 curriculum by bbeaurai.*

# FLY-IN

### Preview
<img width="800" height="450" alt="flyin2" src="https://github.com/user-attachments/assets/e0e37f1f-265a-4930-aae7-effe2d517eb2" />




## Description

FLY-IN is a Python 3.10 drone routing simulation. The program receives a map
describing a graph of connected hubs, then moves a fleet of drones from a
single `start_hub` to a single `end_hub` in as few simulation turns as possible.

The project handles:

- simultaneous drone movement;
- zone capacity with `max_drones`;
- connection metadata with `max_link_capacity`;
- blocked, restricted, normal, start, end, and priority zones;
- route validation before path computation;
- turn-by-turn simulation output;
- graphical visualization with hub states, drones, costs, capacities, zoom, and
  pan controls.

The main objective is not only to find one path, but to schedule many drones
through a constrained graph while avoiding deadlocks, respecting capacities, and
reducing the total number of turns.

## Instructions

### Requirements

- Python 3.10 or later
- A graphical environment able to open an Arcade window
- Dependencies listed in `requirement.txt`

### Install

```bash
make install
```

This creates a local virtual environment and installs the required packages.

### Run

```bash
make run
```

The program opens an interactive menu:

1. choose a map directory inside `maps/`;
2. choose a `.txt` map file;
3. the parser validates the file;
4. `PathChecker` verifies that the end hub can be reached;
5. the pathfinding algorithm computes hub costs;
6. the Arcade simulation window starts.

### Debug

```bash
make debug
```

### Lint

```bash
make lint
make lint-strict
```

`lint-strict` runs:

```bash
flake8 . --exclude venv
mypy . --strict --exclude venv
```

### Clean

```bash
make clean
```

## Map Format

Maps are text files. The first meaningful line must define the number of
drones:

```text
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: obstacleX 5 5 [zone=blocked color=gray]
connection: hub-roof1
connection: hub-corridorA
connection: corridorA-goal [max_link_capacity=2]
```

Supported zone declarations:

- `start_hub: <name> <x> <y> [metadata]`
- `end_hub: <name> <x> <y> [metadata]`
- `hub: <name> <x> <y> [metadata]`

Supported connection declaration:

- `connection: <name1>-<name2> [metadata]`

Metadata:

- `zone=normal`: standard zone, one-turn movement;
- `zone=restricted`: movement into the zone takes two turns;
- `zone=priority`: one-turn movement, preferred when paths have the same cost;
- `zone=blocked`: inaccessible zone;
- `color=<value>`: visual color used by the graphical display;
- `max_drones=<positive_integer>`: maximum drones in a hub;
- `max_link_capacity=<positive_integer>`: maximum drones on a connection.

Comments beginning with `#` are ignored. Hub names must not contain spaces or
dashes because dashes are used to describe connections.

## Simulation Rules

The simulation advances in discrete turns. During each turn, a drone can:

- move to an adjacent hub if capacity allows it;
- enter a restricted hub movement, which takes one extra turn in transit;
- stay in place when moving would break capacity or routing constraints.

The start hub can initially contain all drones. The end hub can contain all
delivered drones. Other hubs respect their `max_drones` capacity.

The simulation prints movements in the required format:

```text
D0-roof1 D1-corridorA
D0-roof2 D1-tunnelB
D0-goal D1-goal
```

Drones that do not move during a turn are omitted from that line. Delivered
drones are no longer moved.

## Algorithm Strategy

The implementation is intentionally object-oriented and avoids graph libraries,
as required by the subject.

### Parsing

`parsing.map_parser.MapParser` reads map files and builds a `Level` object made
of `Hub`, `Connection`, and `Drone` instances. The parser checks the mandatory
structure, metadata syntax, capacities, unique start and end hubs, and invalid
blocked start or end hubs.

### Reachability Check

`algorithm.path_checker.PathChecker` performs a breadth-first search from the
start hub. It ignores blocked hubs and unusable connections. If the end hub
cannot be reached, the program stops before running Dijkstra or the simulation.

### Cost Computation

`algorithm.dijkstra.Algorithm` computes hub values from the end hub backward.
The value represents the best known cost to reach the end:

- `normal`, `priority`, `start`, and `end` count as one turn;
- `restricted` counts as two turns;
- `blocked` hubs are ignored;
- dead ends are penalized.

Priority hubs do not make longer paths artificially better. They are stored in
`priority_score` and are used only as a tie-breaker when two routes have the same
cost.

### Turn Scheduling

`display.round_manager.RoundManager` advances the simulation turn by turn. For
each drone, it chooses the best available neighbor by:

1. refusing blocked or full hubs;
2. avoiding moves that go farther away from the end;
3. preferring lower path cost;
4. preferring higher priority score on equal cost;
5. using downstream load to distribute drones across available routes.

Restricted zones put drones in transit for one turn before they arrive. This
models their two-turn movement cost.

## Visual Representation

The project uses Arcade for graphical feedback. The window displays:

- hubs with textures based on their zone type;
- connection lines with link capacity labels;
- hub names, current drone occupancy, maximum capacity, and computed cost;
- animated drone sprites;
- current round, completion count, and simulation state.

Controls:

- `SPACE`: play or pause;
- `+`: speed up;
- `-`: slow down;
- `R`: reset simulation;
- `Q`: quit;
- mouse drag: pan;
- mouse wheel: zoom.

This visualization helps review the algorithm because blocked zones, priority
routes, congestion, and drone progression can be inspected directly while the
terminal still prints the required turn-by-turn movement log.

## Performance

The subject evaluates performance by the number of simulation turns needed to
deliver all drones. Lower is better.

Reference targets from the subject:

- easy maps: less than 10 turns;
- medium maps: 10 to 30 turns;
- hard maps: less than 60 turns;
- challenger map: optional target is to beat 45 turns.

Current notable result:

- `maps/challenger/01_the_impossible_dream.txt`: 25 drones delivered in 44 turns.

## Project Structure

```text
.
|-- algorithm/
|   |-- dijkstra.py       # Cost computation and priority tie-break
|   `-- path_checker.py   # Reachability check from start to end
|-- display/
|   |-- game_view.py      # Arcade visualization
|   `-- round_manager.py  # Turn-by-turn drone scheduling
|-- parsing/
|   |-- map_parser.py     # File parsing
|   |-- parser.py         # Level construction and validation
|   `-- plateform.py      # Hub, Connection, Drone classes
|-- maps/                 # Provided and custom maps
|-- main.py               # Program entry point
|-- Makefile
`-- requirement.txt
```

## Assets

<img width="900" height="600" alt="1036 8" src="https://github.com/user-attachments/assets/65e0908a-3852-4645-b511-8791f8d8d884" />


## Resources

- Python documentation: https://docs.python.org/3/
- Python `heapq` documentation: https://docs.python.org/3/library/heapq.html
- Python `typing` documentation: https://docs.python.org/3/library/typing.html
- Arcade documentation: https://api.arcade.academy/
- mypy documentation: https://mypy.readthedocs.io/
- flake8 documentation: https://flake8.pycqa.org/
- Dijkstra's algorithm overview: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- Breadth-first search overview: https://en.wikipedia.org/wiki/Breadth-first_search

AI was used to assist with code review,
ensuring strict typing, and organizing the README file. It also provided a few tutorials to help better understand Arcade, etc. Every suggestion made by the AI was reviewed before being accepted.
