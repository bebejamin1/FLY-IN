#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   hub.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/13 15:06:57 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/17 13:39:19 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# from typing import Optional


class Hub():

    def __init__(self, name: str, coord: tuple[int, int],):
        self.name = name
        self.coord = self.coordinate(coord)
        self.zone = "normal"
        self.color = None
        self.max_drones = 1
        self.connection: list[object] = []
        self.value: int = 0

    def start_hub(self):
        pass

    def hub(self):
        pass

    def coordinate(self, coord: tuple[int, int]):
        pass

    def metadata(self, meta: str):
        pass
