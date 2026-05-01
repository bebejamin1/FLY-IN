#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   plateform.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/13 15:06:57 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/01 11:01:45 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


class Hub():

    def __init__(self, name: str, coord: tuple[int, int]):

        self.name = name
        self.coord = coord
        self.zone: str = "normal"
        self.color: str | None = None
        self.max_drones: int = 1
        self.current = 0
        self.connection: list[object] = []
        self.value: int = 1


class Connection():

    def __init__(self, way_1: object, way_2: object):

        self.max_link_capacity: int = 1
        self.way_1: object = way_1
        self.way_2: object = way_2


class Drone():

    def __init__(self, coord: tuple[int, int]):

        self.coord = coord
        self.hub_current: str = None
        self.path: list[str] = []
