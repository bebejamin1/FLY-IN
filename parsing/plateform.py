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


class Hub():

    def __init__(self, name: str, coord: tuple[int, int]) -> None:

        self.name = name
        self.coord = coord
        self.zone: str = "normal"
        self.color: str = ""
        self.max_drones: int = 1
        self.current = 0
        self.connection: list[Connection] = []
        self.value: int = 1


class Connection():

    def __init__(self, way_1: str, way_2: str) -> None:

        self.max_link_capacity: int = 1
        self.way_1: str = way_1
        self.way_2: str = way_2


class Drone():

    def __init__(self, coord: tuple[int, int]) -> None:

        self.coord = coord
        self.hub_current: str = ""
        self.path: list[str] = []
        self.delivered: bool = False
        self.previous_hub: str | None = None
        self.in_transit: bool = False
        self.transit_source: str | None = None
        self.transit_destination: str | None = None
