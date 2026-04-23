#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   drone.py                                             :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/23 13:30:00 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/23 13:22:39 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from typing import Tuple, Optional


class Drone:
    """Classe représentant un drone indépendant sur la carte"""

    def __init__(self, drone_id: int, start_hub_name: str) -> None:
        """
        Initialise un drone

        Args:
            drone_id: Identifiant unique du drone
            start_hub_name: Nom du hub de départ
        """
        self.id = drone_id
        self.current_hub = start_hub_name
        self.path = []
        self.current_position = 0
        self.is_moving = False
        self.delivered = False

    def set_path(self, path: list) -> None:
        """
        Définit le chemin que le drone doit suivre

        Args:
            path: Liste des noms de hubs à traverser
        """
        self.path = path
        self.current_position = 0
        if len(path) > 0:
            self.current_hub = path[0]

    def move_to_next_hub(self) -> bool:
        """
        Déplace le drone vers le prochain hub

        Returns:
            True si le drone a atteint la destination, False sinon
        """
        if not self.path or len(self.path) <= 1:
            self.is_moving = False
            self.delivered = True
            return True

        if self.current_position < len(self.path) - 1:
            self.current_position += 1
            self.current_hub = self.path[self.current_position]
            self.is_moving = True
            return False
        else:
            self.is_moving = False
            self.delivered = True
            return True

    def get_current_coordinates(self) -> Tuple[float, float]:

        return (self.current_position)

    def reset(self, start_hub_name: str) -> None:
        self.current_hub = start_hub_name
        self.path = []
        self.current_position = 0
        self.is_moving = False
        self.delivered = False

    def __repr__(self) -> str:
        return (f"Drone(id={self.id}, hub={self.current_hub},"
                "delivered={self.delivered})")
