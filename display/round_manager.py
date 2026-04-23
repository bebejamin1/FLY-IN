#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   round_manager.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/23 13:30:00 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/23 13:18:21 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from typing import List, Dict
from display.drone import Drone


class RoundManager:
    """Gestionnaire des rounds et du déplacement des drones"""

    def __init__(self, num_drones: int, start_hub_name: str) -> None:
        """
        Initialise le gestionnaire de rounds

        Args:
            num_drones: Nombre de drones à créer
            start_hub_name: Nom du hub de départ pour tous les drones
        """
        self.current_round = 0
        self.drones: List[Drone] = []
        self.start_hub = start_hub_name

        # Crée les drones
        for i in range(num_drones):
            drone = Drone(i, start_hub_name)
            self.drones.append(drone)

    def execute_round(self) -> None:
        """Exécute un round: déplace tous les drones d'un hub au suivant"""
        for drone in self.drones:
            if not drone.delivered:
                drone.move_to_next_hub()
        self.current_round += 1

    def set_drone_path(self, drone_id: int, path: List[str]) -> None:
        """
        Définit le chemin d'un drone

        Args:
            drone_id: ID du drone
            path: Liste des noms des hubs à traverser
        """
        if 0 <= drone_id < len(self.drones):
            self.drones[drone_id].set_path(path)

    def get_drone_current_hub(self, drone_id: int) -> str:
        """Retourne le hub courant d'un drone"""
        if 0 <= drone_id < len(self.drones):
            return self.drones[drone_id].current_hub
        return ""

    def are_all_drones_delivered(self) -> bool:
        """Vérifie si tous les drones ont livré leur cargaison"""
        return all(drone.delivered for drone in self.drones)

    def reset(self) -> None:
        """Réinitialise tous les drones et le compteur de rounds"""
        self.current_round = 0
        for drone in self.drones:
            drone.reset(self.start_hub)

    def get_drone_info(self, drone_id: int) -> Dict:
        """Retourne les informations d'un drone"""
        if 0 <= drone_id < len(self.drones):
            drone = self.drones[drone_id]
            return {
                "id": drone.id,
                "current_hub": drone.current_hub,
                "delivered": drone.delivered,
                "path": drone.path,
                "position": drone.current_position,
            }
        return {}

    def get_all_drones_info(self) -> List[Dict]:
        """Retourne les informations de tous les drones"""
        return [self.get_drone_info(i) for i in range(len(self.drones))]

    def __repr__(self) -> str:
        return (
            f"RoundManager(round={self.current_round}, "
            f"drones={len(self.drones)}, "
            f"delivered={sum(1 for d in self.drones if d.delivered)})"
        )
