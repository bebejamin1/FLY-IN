#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   hub.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/13 15:06:57 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/20 15:13:31 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


class Hub():

    def __init__(self, name: str, coord: tuple[int, int],):
        self.name = name
        self.coord = self.coordinate(coord)
        self.zone = "normal"
        self.color = None
        self.max_drones = 1
        self.connection: list[object] = []
        self.value: int = 0


class Connection():

    def __init__(self, way_1: object, way_2: object):
        self.max_link_capacity: int = 1
        self.way_1: object = way_1
        self.way_2: object = way_2
