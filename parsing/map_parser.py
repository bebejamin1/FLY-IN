#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   map_parser.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/08 12:12:22 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/15 17:34:28 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


from parser import Level


green = "\033[32m\033[1m\033[1m"
red = "\033[31m\033[5m\033[1m"
redp = "\033[31m"
brown = "\033[0;33m"
blue = "\033[38;5;67m"
reset = "\033[0m"


class MapParser():

    def __init__(self, level: str) -> None:
        self.level = f"../{level}"

    def parse_maps(self) -> None:

        try:

            with open(self.level) as f:
                parse = Level()

                for line in f:

                    line = "connection: gate_hell1-gate_hell2"

                    if (line.startswith("nb_drones:")):
                        parse.set_drone(line)

                    if (line.startswith("start_hub")):
                        print(line[11:].split(" "))
                        parse.create_start_hub(line[11:].split(" "))

                    if (line.startswith("hub:")):
                        test = line[5:].split(" ")
                        print(test)
                        parse.create_hub(line[5:].split(" "))

                    if (line.startswith("end_hub")):
                        parse.create_end_hub(line[9:].split(" "))

                    if (line.startswith("connection:")):
                        parse.make_connection(line[12:].split(" "))

                    else:
                        pass

        except (FileNotFoundError) as f:
            print(f"[ERROR] : {f}")


if __name__ == "__main__":
    level = "maps/challenger/01_the_impossible_dream.txt"
    map = MapParser(level)
    map.parse_maps()
