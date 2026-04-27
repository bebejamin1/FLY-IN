#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   round_manager.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/23 13:30:00 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/27 14:10:26 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from parsing.map_parser import Level
from parsing.plateform import Drone


class RoundManager:

    def __init__(self, level: Level) -> None:
        self.level = level
        self.current_round = 0
        self.drones: dict[int, Drone] = {}

        # 1. Initialisation des drones au point de départ
        start_name = self.level.start_hub.name

        # Le hub de départ commence avec tous les drones
        self.level.hub[start_name].current = self.level.nbr_drones

        for i in range(self.level.nbr_drones):
            self.drones[i] = Drone(drone_id=i, start_hub_name=start_name)

    def get_drone_current_hub(self, drone_id: int) -> str:

        if drone_id in self.drones:
            return self.drones[drone_id].current_hub
        return ""

    def execute_round(self) -> list[str]:

        self.current_round += 1
        round_logs = []

        # Pour chaque drone, on tente de le déplacer
        for drone_id, drone in self.drones.items():
            if drone.delivered:
                continue

            current_hub = self.level.hub[drone.current_hub]

            # On cherche le meilleur voisin disponible
            best_next_hub = self._get_best_available_neighbor(current_hub)

            if best_next_hub:
                # --- PHASE DE DÉPLACEMENT ---

                # 1. Le drone quitte son hub actuel (Décrémentation)
                if current_hub.name != self.level.start_hub.name:
                    current_hub.current -= 1

                # 2. Le drone arrive dans le nouveau hub (Incrémentation)
                if best_next_hub.name != self.level.end_hub.name:
                    best_next_hub.current += 1

                # 3. Mise à jour des informations du drone
                drone.current_hub = best_next_hub.name

                # Vérification de la victoire pour ce drone
                if best_next_hub.name == self.level.end_hub.name:
                    drone.delivered = True

                # Format de log demandé par le sujet (ex: D1-roof1)
                round_logs.append(f"D{drone_id}-{best_next_hub.name}")

        return round_logs

    def _get_best_available_neighbor(self, hub) -> object | None:
        """
        Analyse les connexions et retourne le meilleur hub valide.
        Prend en compte la capacité (max_drones) et le coût (value).
        """
        valid_neighbors = []

        for conn in hub.connection:
            # Retrouver le nom de l'autre bout de la connexion
            neighbor_name = conn.way_2 if conn.way_1 == hub.name\
                                       else conn.way_1
            neighbor = self.level.hub[neighbor_name]

            # RÈGLE 1 : Pas bloqué
            if neighbor.zone == "blocked" or neighbor.max_drones == 0:
                continue

            # RÈGLE 2 : Vérification de la capacité (current vs max_drones)
            # Le End Hub a une capacité infinie dans la logique du sujet
            if neighbor.name != self.level.end_hub.name:
                if neighbor.current >= neighbor.max_drones:
                    continue

            # RÈGLE 3 (Bonus) :
            # Vérifier la max_link_capacity de la connexion ici plus tard

            valid_neighbors.append(neighbor)

        if not valid_neighbors:
            return None  # Le drone est bloqué et doit attendre ce tour-ci

        # RÈGLE 4 : On trie les voisins valides par "value" (le coût).
        # Le hub avec la plus petite value sera à l'index 0.
        valid_neighbors.sort(key=lambda x: x.value)

        return valid_neighbors[0]

    def reset(self) -> None:

        self.current_round = 0
        start_name = self.level.start_hub.name

        for hub in self.level.hub.values():
            hub.current = 0
        self.level.hub[start_name].current = self.level.nbr_drones

        for drone in self.drones.values():
            drone.reset(start_name)
