#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   map_parser.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/08 12:12:22 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/17 14:09:50 by bbeaurai           ###   ########.fr      #
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
        self.drones = False

    def parse_maps(self) -> None:

        try:

            with open(self.level) as f:
                parse = Level()

                for line in f:

                    meta = None

                    if (line.startswith("nb_drones:")):
                        parse.set_drone(line[11:])
                        self.drones = True

                    if (line.startswith(("start_hub:", "hub:", "end_hub:",
                                        "connection:"))
                            and self.drones is False):
                        print(f"{red}[ERROR]{reset} : "
                              "The number of drones is not specified first")
                        exit()

                    if (line.startswith("start_hub")):
                        meta = line[line.find("["):]
                        if (meta != 0):
                            line = line[:line.find("[") - 1]
                        parse.create_start_hub(line[11:].strip().split(" "),
                                               meta[:-1])

                    if (line.startswith("hub:")):
                        meta = line[line.find("["):]
                        if (meta != 0):
                            line = line[:line.find("[") - 1]
                        parse.create_hub(line[5:].strip().split(" "),
                                         meta[:-1])

                    if (line.startswith("end_hub")):
                        meta = line[line.find("["):]
                        if (meta != 0):
                            line = line[:line.find("[") - 1]
                        parse.create_end_hub(line[9:].strip().split(" "),
                                             meta[:-1])

                    if (line.startswith("connection:")):
                        parse.make_connection(line[12:].strip().split(" "))

                    else:
                        pass

        except (FileNotFoundError, ValueError, AttributeError) as f:
            print(f"{red}[ERROR]{reset} : {f}")


if __name__ == "__main__":
    level = "maps/challenger/01_the_impossible_dream.txt"
    map = MapParser(level)
    map.parse_maps()
