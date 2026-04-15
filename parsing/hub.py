#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   hub.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/13 15:06:57 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/15 17:22:16 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Hub():

    def __init__(self, name: str, coord: tuple[int, int],
                 meta: list[str] | None):
        self.name = name
        self.coord = self.coordinate(coord)
        self.meta = self.metadata(meta)
        self.connection: list = []
        self.value: int = 0

    def start_hub(self):
        pass

    def hub(self):
        pass

    def coordinate(self, coord: tuple[int, int]):
        pass

    def metadata(self, data: list):
        pass
