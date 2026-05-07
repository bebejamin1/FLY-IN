#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/13 13:30:59 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/05 12:53:02 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from typing import Any

from .plateform import Hub, Connection, Drone


green = "\033[32m\033[1m\033[1m"
red = "\033[31m\033[5m\033[1m"
redp = "\033[31m"
brown = "\033[0;33m"
blue = "\033[38;5;67m"
reset = "\033[0m"


class Level():

    def __init__(self) -> None:
        self.nbr_drones: int = 0
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.hub: dict[str, Hub] = {}
        self.drones: dict[str, Drone] = {}

# ============================= SET DRONES ====================================

    def set_drone(self, line: str) -> None:
        try:

            nbr = int(line)

            if (nbr <= 0):
                raise ValueError("The number of drones must "
                                 f"be a positive number ({nbr})")

            self.nbr_drones = nbr

        except (TypeError, ValueError, IndexError, AttributeError) as e:
            print(f"{red}[ERROR]{reset} : set_drone {e}")
            exit()

# ============================= CLEAN META ====================================

    def clean_meta(self, meta: str) -> dict[str, Any]:
        meta_dict: dict[str, Any] = {}
        valid_meta: list[str] = ["zone", "color", "max_drones"]
        valid_value = [
            ["normal", "blocked", "restricted", "priority"],
            ["orange", "blue", "red", "purple", "black", "brown", "green",
                "gold", "maroon", "darkred", "crimson", "rainbow", "yellow",
                "cyan", "lime", "violet", "magenta", "salmon", "white",
                "gray"],
            []]
        try:

            if (meta == ""):
                return {}

            if not (meta.startswith("[") and meta.endswith("]")):
                raise ValueError(f"Metadata must be enclosed in [] {meta}")

            meta = meta[1:-1]
            meta_split: list[str] = meta.split(" ")

            for m in meta_split:
                if (m.find("=") < 0):
                    raise ValueError(f"Unrecognized meta tag ({m}) "
                                     "must be key=value")

                if not (m[:m.find("=")] in valid_meta):
                    raise ValueError("Invalid meta tag; it must be one of the"
                                     " following: “zone”, \"color\", "
                                     "or “max_drones”")

                if (m[:m.find("=")] == "max_drones"):
                    if (int(m[m.find("=") + 1:]) < 1):
                        raise ValueError("The maximum number of drones "
                                         f"must be greater than 1 ({m})")
                    meta_dict[m[:m.find("=")]] = int(m[m.find("=") + 1:])

                elif not (m[m.find("=") + 1:]
                          in valid_value[valid_meta.index(m[:m.find("=")])]):
                    raise ValueError(f"The value is not good {m}"
                                     " must be [key=value key=value]")

                else:
                    meta_dict[m[:m.find("=")]] = m[m.find("=") + 1:]

        except ValueError as e:
            print(f"{red}[ERROR]{reset} : clean_meta", e)
            exit()

        return (meta_dict)

# ======================== CREATE START HUB ===================================

    def create_start_hub(self, line: list[str], meta: str) -> None:
        if (len(line) != 3):
            raise ValueError(f"create_start_hub {line}")

        try:

            name: str = str(line[0])
            coord: tuple[int, int] = (int(line[1]), int(line[2]))

            if not (self.hub.get(name) is None and self.start_hub is None):
                raise ValueError("start_hub duplicate")

            huber = Hub(name, coord)

            meta_dict: dict[str, Any] = self.clean_meta(meta)

            if (meta_dict):
                for k, v in meta_dict.items():
                    if (k == "zone"):
                        raise ValueError("The start_hub cannot have a meta "
                                         "tag for the zone")
                    setattr(huber, k, v)

            huber.zone = "start"
            self.start_hub = huber
            self.hub[huber.name] = huber

            if (self.start_hub.max_drones == 1):
                self.start_hub.max_drones = self.nbr_drones

            i = 0
            while (i < self.nbr_drones):
                self.drones[f"drone{i}"] = Drone(coord)
                i += 1

        except (ValueError, TypeError) as e:
            print(f"{red}[ERROR]{reset} : ", e)
            exit()

# ========================= CREATE END HUB ====================================

    def create_end_hub(self, line: list[Any], meta: str) -> None:
        if (len(line) != 3):
            raise ValueError(f"create_end_hub {line}")

        try:

            name: str = str(line[0])
            coord: tuple[int, int] = (int(line[1]), int(line[2]))

            if not (self.hub.get(name) is None and self.end_hub is None):
                raise ValueError("start_hub duplicate")

            huber: Hub = Hub(name, coord)

            meta_dict: dict[str, Any] = self.clean_meta(meta)

            if (meta_dict):
                for k, v in meta_dict.items():
                    if (k == "zone"):
                        raise ValueError("The end_hub cannot have a meta tag "
                                         "for the zone")
                    setattr(huber, k, v)

            huber.zone = "end"
            self.end_hub = huber
            self.hub[huber.name] = huber

            if (self.end_hub.max_drones == 1):
                self.end_hub.max_drones = self.nbr_drones

        except (ValueError, TypeError) as e:
            print(f"{red}[ERROR]{reset} : ", e)
            exit()

# =========================== CREATE HUB ======================================

    def create_hub(self, line: list[Any], meta: str) -> None:
        if (len(line) != 3):
            raise ValueError(f"create_hub {line}")

        try:

            name: str = str(line[0])
            coord: tuple[int, int] = (int(line[1]), int(line[2]))

            if not (self.hub.get(name) is None):
                raise ValueError("Hub duplicate")

            huber = Hub(name, coord)

            meta_dict: dict[str, Any] = self.clean_meta(meta)

            if (meta_dict):
                for k, v in meta_dict.items():
                    setattr(huber, k, v)
                    if (v == "blocked"):
                        huber.max_drones = 0
                    if (v == "restricted"):
                        huber.value = 2

            self.hub[huber.name] = huber

        except (ValueError, TypeError) as e:
            print(f"{red}[ERROR]{reset} : ", e)
            exit()

# ===================== CLEAN META CONNECTION =================================

    def clean_meta_connection(self, meta: str) -> int:
        try:
            if (meta == ""):
                return (-1)

            if not (meta.startswith("[") and meta.endswith("]")):
                return (-1)

            return (int(meta[meta.find("=") + 1: - 1]))

        except ValueError:
            print(f"{red}[ERROR]{reset} : max_link_capacity must be "
                  "a positive integer")
            exit()
# ========================== MAKE CONNECTION ==================================

    def make_connection(self, line: list[Any]) -> None:
        if (len(line) > 2 or len(line) < 1):
            raise ValueError(f"create_hub {line}")

        try:
            meta = -1
            meta_link: int = -1
            link = line[0].split("-")

            if (len(line) == 2):
                meta = line[1]
                meta_link = self.clean_meta_connection(meta)

            way_1: str = link[0]
            way_2: str = link[1]

            if not (self.hub[way_1] or self.hub[way_2]):
                raise ValueError("The connection cannot be established; "
                                 f"hub is missing ({way_1} or {way_2})")

            connect: Connection = Connection(way_1, way_2)

            if (meta_link > 1):
                connect.max_link_capacity = meta_link

            self.hub[way_1].connection.append(connect)
            self.hub[way_2].connection.append(connect)

        except ValueError as e:
            print(f"{red}[ERROR]{reset} : ", e)
            exit()
        except TypeError:
            print(f"{red}[ERROR]{reset} : Invalid connection;"
                  f" hub not recognized {line}")
            exit()
        except (NameError, KeyError) as e:
            print(f"{red}[ERROR]{reset} : {line}, {e}")
            exit()
