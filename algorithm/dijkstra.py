#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   dijkstra.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/27 16:38:14 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/05 12:56:47 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Weighted path scoring algorithm used to guide drone movement."""

from heapq import heappop, heappush

from parsing.parser import Level
from parsing.plateform import Hub


UNREACHABLE_VALUE = 888888


class Algorithm():
    """Compute routing values for each hub in a parsed level.

    Attributes:
        level: Level whose hubs will receive route values.
        start: Name of the start hub.
        end: Name of the end hub.
    """

    def __init__(self, level: Level) -> None:
        """Initialize the algorithm with a level that has start and end hubs.

        Args:
            level: Parsed level to score.

        Returns:
            None.
        """
        self.level = level

        if (self.level.start_hub is None):
            raise ValueError("start_hub missing")
        if (self.level.end_hub is None):
            raise ValueError("end_hub missing")

        self.start: str = level.hub[self.level.start_hub.name].name
        self.end: str = level.hub[self.level.end_hub.name].name

# ============================= DEAD END ======================================

    def penalize_dead_ends(self) -> None:
        """Mark non-terminal dead-end hubs as unreachable.

        Returns:
            None.
        """
        for hub in self.level.hub.values():

            if (hub.name == self.start or hub.name == self.end):
                continue

            valid_connections_count = 0
            for con in hub.connection:
                neighbor_name = con.way_2 if con.way_1 == hub.name\
                                          else con.way_1
                neighbor_hub = self.level.hub[neighbor_name]
                if (neighbor_hub.zone != "blocked"):
                    valid_connections_count += 1

            if (valid_connections_count == 1):
                hub.value = UNREACHABLE_VALUE
                hub.priority_score = 0

# ============================== VALUE ========================================

    def determine_value(self, hub: Hub) -> int:
        """Return the movement cost associated with a hub.

        Args:
            hub: Hub whose traversal cost should be evaluated.

        Returns:
            Cost value used by the route-scoring algorithm.
        """
        if (hub.zone == "restricted"):
            return (2)

        return (1)

    def determine_priority(self, hub: Hub, next_hub: Hub) -> int:
        """Calculate priority inherited from the next hub in a route.

        Args:
            hub: Hub being evaluated.
            next_hub: Neighbor closer to the destination.

        Returns:
            Priority score propagated back through the route.
        """
        priority_score = next_hub.priority_score

        if (hub.zone == "priority"):
            priority_score += 1

        return (priority_score)

# ============================= NEIGHBOR ======================================

    def find_neighbor(self, hub: Hub) -> list[Hub]:
        """Find passable hubs directly connected to a hub.

        Args:
            hub: Hub whose neighbors should be inspected.

        Returns:
            List of connected hubs that are not blocked.
        """
        neighbor: list[Hub] = []

        for con in hub.connection:

            neighbor_name = con.way_2 if con.way_1 == hub.name else con.way_1
            neighbor_hub = self.level.hub[neighbor_name]

            if (neighbor_hub.zone != "blocked"
                    and con.max_link_capacity != 0):

                neighbor.append(neighbor_hub)

        return (neighbor)

    def is_better_path(
        self, hub: Hub, value: int, priority_score: int
    ) -> bool:
        """Check whether a candidate route improves a hub score.

        Args:
            hub: Hub whose current score should be compared.
            value: Candidate route cost.
            priority_score: Candidate priority score.

        Returns:
            True when the candidate route is preferred, otherwise False.
        """
        if (value < hub.value):
            return (True)

        if (value == hub.value and priority_score > hub.priority_score):
            return (True)

        return (False)

# =============================== ALGO ========================================

    def make_algo(self) -> Level:
        """Assign route values and priorities to every reachable hub.

        Returns:
            The same level instance with updated hub values and priorities.
        """
        queue: list[tuple[int, int, str]] = []
        end_hub = self.level.hub[self.end]

        for hub in self.level.hub.values():
            hub.value = UNREACHABLE_VALUE
            hub.priority_score = 0

        end_hub.value = self.determine_value(end_hub)
        heappush(queue, (end_hub.value, -end_hub.priority_score,
                         end_hub.name))

        while (queue):
            value, priority_score, curr_name = heappop(queue)
            curr = self.level.hub[curr_name]

            if (value != curr.value
                    or -priority_score != curr.priority_score):
                continue

            if (curr.name == self.start):
                continue

            neighbor = self.find_neighbor(curr)

            for n in neighbor:
                new_value = curr.value + self.determine_value(n)
                new_priority_score = self.determine_priority(n, curr)

                better_path = self.is_better_path(
                    n, new_value, new_priority_score
                )

                if (better_path):
                    n.value = new_value
                    n.priority_score = new_priority_score
                    heappush(queue, (n.value, -n.priority_score, n.name))

        self.penalize_dead_ends()

        return (self.level)
