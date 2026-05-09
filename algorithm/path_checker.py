#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   path_checker.py                                      :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/05/08 00:00:00 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/08 00:00:00 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Reachability checks for parsed levels before running the simulation."""

from parsing.parser import Level
from parsing.plateform import Hub


class PathChecker():
    """Check whether the start hub can reach the end hub.

    Attributes:
        level: Parsed level to inspect.
        start: Name of the start hub.
        end: Name of the end hub.
    """

    def __init__(self, level: Level) -> None:
        """Initialize the checker with a level containing start and end hubs.

        Args:
            level: Parsed level to validate for reachability.

        Returns:
            None.
        """
        self.level = level

        if (self.level.start_hub is None):
            raise ValueError("start_hub missing")
        if (self.level.end_hub is None):
            raise ValueError("end_hub missing")

        self.start: str = self.level.start_hub.name
        self.end: str = self.level.end_hub.name

# ============================= NEIGHBOR ======================================

    def find_neighbor(self, hub: Hub, visited: set[str]) -> list[Hub]:
        """Find unvisited passable neighbors for breadth-first search.

        Args:
            hub: Hub currently being explored.
            visited: Hub names that have already been queued or visited.

        Returns:
            List of reachable neighboring hubs.
        """
        neighbor: list[Hub] = []

        for con in hub.connection:

            neighbor_name = con.way_2 if con.way_1 == hub.name else con.way_1
            neighbor_hub = self.level.hub[neighbor_name]

            if (neighbor_name not in visited
                    and neighbor_hub.zone != "blocked"
                    and con.max_link_capacity != 0):

                neighbor.append(neighbor_hub)

        return (neighbor)

# =============================== ALGO ========================================

    def is_path_possible(self) -> bool:
        """Determine whether at least one route exists from start to end.

        Returns:
            True when the destination hub is reachable, otherwise False.
        """
        queue: list[Hub] = [self.level.hub[self.start]]
        visited: set[str] = {self.start}
        head = 0

        while (head < len(queue)):
            curr = queue[head]
            head += 1

            if (curr.name == self.end):
                return (True)

            neighbor = self.find_neighbor(curr, visited)

            for n in neighbor:
                visited.add(n.name)
                queue.append(n)

        return (False)
