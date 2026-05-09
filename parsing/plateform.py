#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   plateform.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/13 15:06:57 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/05 11:47:04 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Domain objects used to model hubs, connections, and drones."""


class Hub():
    """Represent a stop in the delivery network.

    Attributes:
        name: Unique hub identifier.
        coord: Grid coordinates used by the parser, algorithm, and display.
        zone: Hub behavior category, such as normal, start, end, or blocked.
        color: Optional display color name.
        max_drones: Maximum number of drones allowed on the hub at once.
        current: Number of drones currently occupying the hub.
        connection: Connections linked to this hub.
        value: Routing cost assigned by the path algorithm.
        priority_score: Priority score assigned by the path algorithm.
    """

    def __init__(self, name: str, coord: tuple[int, int]) -> None:
        """Initialize a hub with default routing and display properties.

        Args:
            name: Unique name for the hub.
            coord: Grid coordinates of the hub.

        Returns:
            None.
        """
        self.name = name
        self.coord = coord
        self.zone: str = "normal"
        self.color: str = ""
        self.max_drones: int = 1
        self.current = 0
        self.connection: list[Connection] = []
        self.value: int = 1
        self.priority_score: int = 0


class Connection():
    """Represent an undirected link between two hubs.

    Attributes:
        current: Number of drones using the link during the current round.
        max_link_capacity: Maximum drones allowed on the link per round.
        way_1: Name of the first linked hub.
        way_2: Name of the second linked hub.
    """

    def __init__(self, way_1: str, way_2: str) -> None:
        """Initialize a connection with the default link capacity.

        Args:
            way_1: Name of one endpoint hub.
            way_2: Name of the other endpoint hub.

        Returns:
            None.
        """
        self.current: int = 0
        self.max_link_capacity: int = 1
        self.way_1: str = way_1
        self.way_2: str = way_2


class Drone():
    """Represent a drone moving through the hub network.

    Attributes:
        coord: Starting grid coordinates for the drone.
        hub_current: Name of the current hub, or IN_TRANSIT while moving.
        path: Reserved path list for planned routes.
        delivered: Whether the drone has reached the end hub.
        previous_hub: Last hub visited before the current hub.
        in_transit: Whether the drone is crossing a restricted hub edge.
        transit_source: Source hub used for a restricted transit step.
        transit_destination: Destination hub used for a restricted transit step.
    """

    def __init__(self, coord: tuple[int, int]) -> None:
        """Initialize a drone at its starting coordinates.

        Args:
            coord: Grid coordinates where the drone starts.

        Returns:
            None.
        """
        self.coord = coord
        self.hub_current: str = ""
        self.path: list[str] = []
        self.delivered: bool = False
        self.previous_hub: str | None = None
        self.in_transit: bool = False
        self.transit_source: str | None = None
        self.transit_destination: str | None = None
