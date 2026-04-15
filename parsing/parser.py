#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/13 13:30:59 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/15 17:33:43 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


from hub import Hub


green = "\033[32m\033[1m\033[1m"
red = "\033[31m\033[5m\033[1m"
redp = "\033[31m"
brown = "\033[0;33m"
blue = "\033[38;5;67m"
reset = "\033[0m"


class Level():

    def __init__(self):
        self.nbr_drone: int = 0
        self.start_hub: Hub = None
        self.end_hub: Hub = None
        self.hub: Hub = {}

# ============================= SET DRONES ====================================

    def set_drone(self, line: str) -> None:
        try:

            nbr = int(line[11:])

            if (nbr < 0):
                raise ValueError("The number of drones must "
                                 f"be a positive number ({nbr})")

            self.nbr_drone = nbr

        except (TypeError, ValueError, IndexError) as e:
            print(f"[ERROR] : {e}")

# ======================== CREATE START HUB ===================================

    def create_start_hub(self, line: list) -> None:
        try:

            print(line)

        except ValueError as e:
            raise (e)

# ========================= CREATE END HUB ====================================

    def create_end_hub(self, line: list) -> None:
        pass

# =========================== CREATE HUB ======================================

    def create_hub(self, line: list) -> None:
        pass

# ========================== MAKE CONNECTION ==================================

    def make_connection(self, line: list) -> None:
        pass


if __name__ == "__main__":
    test = Level()
    line = ["start", "0", "0", "[color=green max_drones=25]"]
    drone = test.create_start_hub(line)
    print(test.nbr_drone)
