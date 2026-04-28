#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   dijkstra.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/27 16:38:14 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/28 14:09:03 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Algorithm():

    def __init__(self, level: object) -> None:
        self.level = level
        self.end: str = level.hub[self.level.end_hub.name].name

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
            value = 500 + before

        elif (hub.zone == "blocked"):
            value = 15000 + before

        else:
            value = 2 + before

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

        return (self.level)


# gros cul de sac
