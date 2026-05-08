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

from parsing.parser import Level
from parsing.plateform import Hub


class PathChecker():

    def __init__(self, level: Level) -> None:
        self.level = level

        if (self.level.start_hub is None):
            raise ValueError("start_hub missing")
        if (self.level.end_hub is None):
            raise ValueError("end_hub missing")

        self.start: str = self.level.start_hub.name
        self.end: str = self.level.end_hub.name

# ============================= NEIGHBOR ======================================

    def find_neighbor(self, hub: Hub, visited: set[str]) -> list[Hub]:

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
