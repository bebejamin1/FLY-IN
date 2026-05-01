#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   map_parser.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/08 12:12:22 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/01 11:01:55 by bbeaurai           ###   ########.fr      #
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

            with open(self.level, "r") as f:

                if (len(f.read()) <= 10):
                    raise ValueError("The file is empty, you idiot")

                parse = Level()

                f.seek(0)
                for line in f:

                    if (line.startswith("nb_drones:")):
                        parse.set_drone(line[11:])
                        self.drones = True

                    if (line.startswith(("start_hub:", "hub:", "end_hub:",
                                        "connection:"))
                            and self.drones is False):
                        raise ValueError(f"{red}[ERROR]{reset} : "
                              "The number of drones is not specified first")

                    if (line.startswith("start_hub")):
                        meta = ""

                        if ("[" in line):
                            index_crochet = line.find("[")
                            meta = line[index_crochet:]
                            line = line[:index_crochet]

                        parse.create_start_hub(line[11:].strip().split(" "),
                                               meta[:-1])

                    if (line.startswith("hub:")):
                        meta = ""

                        if ("[" in line):
                            index_crochet = line.find("[")
                            meta = line[index_crochet:]
                            line = line[:index_crochet]

                        parse.create_hub(line[5:].strip().split(" "),
                                         meta[:-1])

                    if (line.startswith("end_hub")):
                        meta = ""

                        if ("[" in line):
                            index_crochet = line.find("[")
                            meta = line[index_crochet:]
                            line = line[:index_crochet]

                        parse.create_end_hub(line[9:].strip().split(" "),
                                             meta[:-1])

                    if (line.startswith("connection:")):
                        parse.make_connection(line[12:].strip().split(" "))

                    else:
                        pass

                if (parse.start_hub is None):
                    raise ValueError("There must be an start hub")

                if (parse.start_hub.zone == "blocked"):
                    raise ValueError("The start cannot be blocked")

                if (len(parse.start_hub.connection) == 0):
                    raise ValueError("The start_hub has no connections")

                if (parse.end_hub is None):
                    raise ValueError("There must be an end hub")

                if (parse.end_hub.zone == "blocked"):
                    raise ValueError("The end cannot be blocked")

                if (len(parse.end_hub.connection) == 0):
                    raise ValueError("The end_hub has no connections")

                if (parse.start_hub.coord == parse.end_hub.coord):
                    raise ValueError("The start_hub and end_hub cannot be part"
                                     " of the same problem")

                if (parse.start_hub.max_drones < parse.nbr_drones
                        or parse.end_hub.max_drones < parse.nbr_drones):
                    raise ValueError("There are too many drones to place on "
                                     "the start and/or end hubs")

                return (parse)

        except (ValueError, AttributeError) as e:
            print(f"{red}[ERROR]{reset} : {e}")
            exit()

        except FileNotFoundError:
            print(f"{red}[ERROR]{reset} : File missing; """
                  "there must be a parent file named “maps” "
                  "that contains text files")
            exit()
