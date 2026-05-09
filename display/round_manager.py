#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   round_manager.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/23 13:30:00 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/05 12:58:26 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Round-based simulation logic for moving drones between hubs."""

from typing import cast

from parsing.parser import Level
from parsing.plateform import Hub, Drone, Connection


class RoundManager:
    """Advance drone positions through the scored hub network.

    Attributes:
        level: Level whose drones and hubs are simulated.
        current_round: Number of rounds already executed.
        drones: Drones indexed by their generated names.
        start_hub: Hub where all drones begin.
        end_hub: Hub where delivery is completed.
    """

    def __init__(self, level: Level) -> None:
        """Initialize the round manager and place drones at the start hub.

        Args:
            level: Parsed and scored level to simulate.

        Returns:
            None.
        """
        self.level = level
        self.current_round: int = 0
        self.drones: dict[str, Drone] = self.level.drones

        if (self.level.start_hub is None):
            raise ValueError("start_hub missing")
        if (self.level.end_hub is None):
            raise ValueError("end_hub missing")

        self.start_hub: Hub = self.level.start_hub
        self.end_hub: Hub = self.level.end_hub

        start_name: str = self.start_hub.name
        self.level.hub[start_name].current = self.level.nbr_drones

        for drone in self.drones.values():
            drone.hub_current = start_name
            drone.delivered = False
            drone.previous_hub = None
            drone.in_transit = False
            drone.transit_source = None
            drone.transit_destination = None

# ========================== EXECUTE ROUND ====================================

    def execute_round(self) -> list[str]:
        """Move each eligible drone once and record round output logs.

        Returns:
            Movement logs formatted for terminal output.
        """
        self.current_round += 1
        round_logs = []
        self._reset_connection_currents()

        for drone_key, drone in self.drones.items():
            try:
                d_id = int(drone_key.replace("drone", ""))
            except ValueError:
                d_id = 0

            if (drone.delivered):
                continue

            if (drone.in_transit):
                drone.in_transit = False
                source_name = cast(str, drone.transit_source)
                destination_name = cast(str, drone.transit_destination)
                drone.previous_hub = source_name
                drone.hub_current = destination_name

                if (drone.hub_current == self.end_hub.name):
                    drone.delivered = True

                round_logs.append(f"D{d_id}-{drone.hub_current}")
                continue

            current_hub = self.level.hub[drone.hub_current]
            best_move = self._get_best_available_neighbor(
                current_hub, drone.previous_hub
            )

            if (best_move):
                best_next_hub, connection = best_move

                current_hub.current -= 1
                connection.current += 1

                if (best_next_hub.zone == "restricted"):
                    drone.in_transit = True
                    drone.transit_source = current_hub.name
                    drone.transit_destination = best_next_hub.name
                    drone.hub_current = "IN_TRANSIT"

                    best_next_hub.current += 1

                    round_logs.append(f"D{d_id}-{current_hub.name}-"
                                      f"{best_next_hub.name}")

                else:
                    drone.previous_hub = current_hub.name
                    drone.hub_current = best_next_hub.name

                    best_next_hub.current += 1

                    if (best_next_hub.name == self.end_hub.name):
                        drone.delivered = True

                    round_logs.append(f"D{d_id}-{best_next_hub.name}")

        return (round_logs)

# =========================== GET NEIGHBOR ====================================

    def _get_best_available_neighbor(
        self, hub: Hub, previous_hub_name: str | None
    ) -> tuple[Hub, Connection] | None:
        """Choose the best valid next move from a hub.

        Args:
            hub: Current hub of the drone being moved.
            previous_hub_name: Hub visited immediately before the current one.

        Returns:
            Pair of the chosen neighbor and connection, or None if blocked.
        """
        valid_neighbors: list[tuple[Hub, Connection]] = []

        for conn in hub.connection:
            neighbor_name = conn.way_2 if conn.way_1 == hub.name\
                                       else conn.way_1

            if (neighbor_name == previous_hub_name):
                continue

            if (conn.current >= conn.max_link_capacity):
                continue

            neighbor = self.level.hub[neighbor_name]

            if (neighbor.zone == "blocked"
                    or getattr(neighbor, 'max_drones', 1) == 0):
                continue

            if (neighbor.value > hub.value):
                continue

            if (neighbor.name != self.end_hub.name):
                if (neighbor.current >= neighbor.max_drones):
                    continue

            valid_neighbors.append((neighbor, conn))

        if (not valid_neighbors):
            return (None)

        valid_neighbors.sort(key=self._neighbor_sort_key)

        return (valid_neighbors[0])

    def _neighbor_sort_key(
        self, move: tuple[Hub, Connection]
    ) -> tuple[int, int, float, str]:
        """Build a stable ordering key for candidate drone moves.

        Args:
            move: Candidate neighbor and connection pair.

        Returns:
            Tuple used to sort by cost, priority, load, and hub name.
        """
        neighbor = move[0]

        return (neighbor.value, -neighbor.priority_score,
                self._get_downstream_load(neighbor), neighbor.name)

    def _get_downstream_load(self, hub: Hub) -> float:
        """Estimate local congestion downstream from a candidate hub.

        Args:
            hub: Hub from which downstream load should be sampled.

        Returns:
            Aggregate load score across nearby reachable hubs.
        """
        total_load = 0.0
        queue: list[tuple[Hub, int]] = [(hub, 0)]
        visited: set[str] = {hub.name}
        head = 0

        while (head < len(queue)):
            current_hub, depth = queue[head]
            head += 1

            max_drones = max(1, current_hub.max_drones)
            if (current_hub.name == self.end_hub.name):
                max_drones = self.level.nbr_drones
            total_load += current_hub.current / max_drones

            if (depth >= 3):
                continue

            for conn in current_hub.connection:
                neighbor_name = conn.way_2 if conn.way_1 == current_hub.name\
                                           else conn.way_1

                if (neighbor_name in visited):
                    continue

                neighbor = self.level.hub[neighbor_name]

                if (neighbor.zone == "blocked"
                        or neighbor.value > current_hub.value):
                    continue

                visited.add(neighbor_name)
                queue.append((neighbor, depth + 1))

        return (total_load)

    def _reset_connection_currents(self) -> None:
        """Clear per-round usage counters on every unique connection.

        Returns:
            None.
        """
        visited: set[int] = set()

        for hub in self.level.hub.values():
            for conn in hub.connection:
                conn_id = id(conn)
                if (conn_id in visited):
                    continue
                visited.add(conn_id)
                conn.current = 0

# ============================== RESET ========================================

    def reset(self) -> None:
        """Restore all drones, hubs, and connections to the initial round state.

        Returns:
            None.
        """
        self.current_round = 0
        start_name = self.start_hub.name

        for hub in self.level.hub.values():
            hub.current = 0
        self.level.hub[start_name].current = self.level.nbr_drones
        self._reset_connection_currents()

        for drone in self.drones.values():
            drone.hub_current = start_name
            drone.delivered = False
            drone.previous_hub = None
            drone.in_transit = False
