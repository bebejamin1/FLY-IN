#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   map_parser.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/08 12:12:22 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/17 15:52:52 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


from .parser import Level


green = "\033[32m\033[1m\033[1m"
red = "\033[31m\033[5m\033[1m"
redp = "\033[31m"
brown = "\033[0;33m"
blue = "\033[38;5;67m"
reset = "\033[0m"


class MapParser():

    def __init__(self, level: str) -> None:
        self.level = f"{level}"
        self.drones = False

    def parse_maps(self) -> Level:

        try:

            with open(self.level) as f:

                if (len(f.read()) <= 10):
                    raise ValueError("The file is empty, you idiot")

                parse = Level()

                for line in f:

                    meta = None

                    if (line.startswith("nb_drones:")):
                        parse.set_drone(line[11:])
                        print(parse.nbr_drones)
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

                if ():
                    pass
                print(parse.nbr_drones)
                print(parse.start_hub)
                print(parse.end_hub)
                print(parse.hub)
                if (parse.start_hub is None):
                    raise ValueError("There must be an start hub")

                if (len(parse.start_hub.connection) == 0):
                    raise ValueError("The start_hub has no connections")

                if (parse.end_hub is None):
                    raise ValueError("There must be an end hub")

                if (len(parse.end_hub.connection) == 0):
                    raise ValueError("The end_hub has no connections")

                return (parse)

        except (FileNotFoundError, ValueError, AttributeError) as f:
            print(f"{red}[ERROR]{reset} : {f}")


if __name__ == "__main__":
    level = "maps/error/blocked.txt"
    map = MapParser(level)
    level_data = map.parse_maps()
    print(level_data)
