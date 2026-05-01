#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   round_manager.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/23 13:30:00 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/01 10:45:54 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from parsing.map_parser import Level


class RoundManager:

    def __init__(self, level: Level) -> None:
        self.level = level
        self.current_round = 0
        self.drones = self.level.drones

        start_name = self.level.start_hub.name
        self.level.hub[start_name].current = self.level.nbr_drones

        for drone_key, drone in self.drones.items():
            drone.hub_current = start_name
            drone.delivered = False
            drone.previous_hub = None
            drone.in_transit = False
            drone.transit_source = None
            drone.transit_destination = None

# ========================== EXECUTE ROUND ====================================

    def execute_round(self) -> list[str]:
        self.current_round += 1
        round_logs = []

        for drone_key, drone in self.drones.items():
            try:
                d_id = int(drone_key.replace("drone", ""))
            except ValueError:
                d_id = 0

            if drone.delivered:
                continue

            if drone.in_transit:
                drone.in_transit = False
                drone.previous_hub = drone.transit_source
                drone.hub_current = drone.transit_destination

                if drone.hub_current == self.level.end_hub.name:
                    drone.delivered = True

                round_logs.append(f"D{d_id}-{drone.hub_current}")
                continue

            current_hub = self.level.hub[drone.hub_current]
            best_next_hub = self._get_best_available_neighbor(
                    current_hub, drone.previous_hub
                                                             )

            if best_next_hub:

                current_hub.current -= 1

                if best_next_hub.zone == "restricted":
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

                    if best_next_hub.name == self.level.end_hub.name:
                        drone.delivered = True

                    round_logs.append(f"D{d_id}-{best_next_hub.name}")

        return round_logs

# =========================== GET NEIGHBOR ====================================

    def _get_best_available_neighbor(self, hub: object,
                                     previous_hub_name: str) -> object | None:
        valid_neighbors = []
        all_possible_neighbors = []

        for conn in hub.connection:
            neighbor_name = conn.way_2 if conn.way_1 == hub.name\
                                       else conn.way_1

            if neighbor_name == previous_hub_name:
                continue

            neighbor = self.level.hub[neighbor_name]

            if (neighbor.zone == "blocked"
                    or getattr(neighbor, 'max_drones', 1) == 0):
                continue
            
            all_possible_neighbors.append(neighbor)

            if (neighbor.name != self.level.end_hub.name):
                if (neighbor.current >= neighbor.max_drones):
                    continue

            valid_neighbors.append(neighbor)

        if not all_possible_neighbors:
            return None

        all_possible_neighbors.sort(key=lambda x: x.value)
        absolute_best = all_possible_neighbors[0]

        if not valid_neighbors:
            return None

        valid_neighbors.sort(key=lambda x: x.value)
        best_available = valid_neighbors[0]

        MAX_WEIGHT_DIFF = 50

        if (absolute_best.name != self.level.end_hub.name and
                absolute_best.current >= absolute_best.max_drones):
            
            if (best_available.value - absolute_best.value) >= MAX_WEIGHT_DIFF:
                return None

        return best_available

# ============================== RESET ========================================

    def reset(self) -> None:
        self.current_round = 0
        start_name = self.level.start_hub.name

        for hub in self.level.hub.values():
            hub.current = 0
        self.level.hub[start_name].current = self.level.nbr_drones

        for drone in self.drones.values():
            drone.hub_current = start_name
            drone.delivered = False
            drone.previous_hub = None
            drone.in_transit = False
