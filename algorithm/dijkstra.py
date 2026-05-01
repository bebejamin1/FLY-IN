#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   dijkstra.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/27 16:38:14 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/01 11:37:29 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Algorithm():

    def __init__(self, level: object) -> None:
        self.level = level
        self.end: str = level.hub[self.level.end_hub.name].name

# ============================= DEAD END ======================================

    def penalize_dead_ends(self) -> None:

        for hub in self.level.hub.values():

            if hub.name == self.level.start_hub.name or hub.name == self.level.end_hub.name:
                continue

            valid_connections_count = 0
            for con in hub.connection:
                neighbor_name = con.way_2 if con.way_1 == hub.name else con.way_1
                neighbor_hub = self.level.hub[neighbor_name]
                if neighbor_hub.zone != "blocked":
                    valid_connections_count += 1

            if valid_connections_count == 1:
                hub.value = 888888

# ============================== VALUE ========================================

    def determine_value(self, hub: object, save_path: list[str]) -> int:

        value = 0

        if (save_path):
            before = self.level.hub[save_path[-1]].value
        else:
            before = 1

        if (hub.zone == "priority"):
            value = 0 + before

        elif (hub.zone == "normal"):
            value = 5 + before

        elif (hub.zone == "restricted"):
            value = 25 + before

        elif (hub.zone == "blocked"):
            value = 150 + before

        else:
            value = 1 + before

        return (value)

# ============================= NEIGHBOR ======================================

    def find_neighbor(self, hub: object, save_path: list[str]) -> list[object]:

        neighbor = []

        for con in hub.connection:

            neighbor_name = con.way_2 if con.way_1 == hub.name else con.way_1
            neighbor_hub = self.level.hub[neighbor_name]

            if (neighbor_name not in save_path and
                neighbor_hub.zone != "blocked" and
                    con.max_link_capacity != 0 and
                    neighbor_hub.value <= 2):

                neighbor.append(neighbor_hub)

        return (neighbor)

# =============================== ALGO ========================================

    def make_algo(self) -> object:

        queue: list[object] = [self.level.hub[self.end]]
        save_path: list[str] = []

        head: int = 0
        while (head < len(queue)):

            curr = queue[head]
            head += 1

            neighbor = self.find_neighbor(curr, save_path)

            if (neighbor):
                for n in neighbor:
                    queue.append(n)

            curr.value = self.determine_value(curr, save_path)

            save_path.append(curr.name)

        self.penalize_dead_ends()

        return (self.level)
