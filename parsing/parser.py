#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/13 13:30:59 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/12 16:28:30 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Parsing helpers that build an in-memory level from map tokens."""

from typing import Any

from .plateform import Hub, Connection, Drone


green = "\033[32m\033[1m\033[1m"
red = "\033[31m\033[5m\033[1m"
redp = "\033[31m"
brown = "\033[0;33m"
blue = "\033[38;5;67m"
reset = "\033[0m"


class Level():
    """Store every parsed object that defines one playable level.

    Attributes:
        nbr_drones: Number of drones declared by the map file.
        start_hub: Starting hub for all drones.
        end_hub: Delivery destination hub.
        hub: Hubs indexed by their names.
        drones: Drones indexed by generated drone identifiers.
    """

    def __init__(self) -> None:
        """Initialize an empty level container.

        Returns:
            None.
        """
        self.nbr_drones: int = 0
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.hub: dict[str, Hub] = {}
        self.drones: dict[str, Drone] = {}

# ============================= SET DRONES ====================================

    def set_drone(self, line: str) -> None:
        """Parse and store the number of drones declared in a map file.

        Args:
            line: Raw text value found after the nb_drones marker.

        Returns:
            None.
        """
        try:

            nbr = int(line)

            if (nbr <= 0):
                raise ValueError("The number of drones must "
                                 f"be a positive number ({nbr})")

            if (nbr > 500):
                raise ValueError("The number of drones should "
                                 f"not be too high max 500 : ({nbr})")

            self.nbr_drones = nbr

        except (TypeError, ValueError, IndexError, AttributeError) as e:
            print(f"{red}[ERROR]{reset} : set_drone {e}")
            print(line)
            exit()

# ============================= CLEAN META ====================================

    def clean_meta(self, meta: str) -> dict[str, Any]:
        """Validate and normalize hub metadata from a raw bracketed string.

        Args:
            meta: Raw metadata string, such as [color=blue max_drones=2].

        Returns:
            Dictionary of validated metadata values keyed by metadata name.
        """
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
                    if (int(m[m.find("=") + 1:]) > self.nbr_drones):
                        raise ValueError("max_link_capacity must be less "
                                         "than or equal to the number "
                                         "of drones")
                    meta_dict[m[:m.find("=")]] = int(m[m.find("=") + 1:])

                elif not (m[m.find("=") + 1:]
                          in valid_value[valid_meta.index(m[:m.find("=")])]):
                    raise ValueError(f"The value is not good {m}"
                                     " must be [key=value key=value]")

                else:
                    meta_dict[m[:m.find("=")]] = m[m.find("=") + 1:]

        except ValueError as e:
            print(f"{red}[ERROR]{reset} : check clean_meta in "
                  "parser" + "\n", e)
            print(meta)
            exit()

        return (meta_dict)

# ======================== CREATE START HUB ===================================

    def create_start_hub(self, line: list[str], meta: str) -> None:
        """Create the start hub and spawn the level drones at its coordinates.

        Args:
            line: Tokenized start hub definition containing name, x, and y.
            meta: Raw metadata string attached to the start hub.

        Returns:
            None.
        """
        if (len(line) != 3):
            raise ValueError(f"incorrect format {line} {meta}")

        try:

            name: str = str(line[0])
            coord: tuple[int, int] = (int(line[1]), int(line[2]))

            if (coord[0] > 100 or coord[1] > 100):
                raise ValueError("It is not possible to enter coordinates "
                                 f"greater than 100. \n{name}: {coord}")

            if not (self.hub.get(name) is None and self.start_hub is None):
                raise ValueError("start_hub duplicate")

            huber = Hub(name, coord)

            meta_dict: dict[str, Any] = self.clean_meta(meta)

            if (meta_dict):
                for k, v in meta_dict.items():
                    if (v == "blocked"):
                        raise ValueError("start_hub cannot be blocked")
                    if (k == "zone"):
                        print(f"{redp}start_hub will not take the zone change "
                              f"into account{reset}")
                    setattr(huber, k, v)

            for h in self.hub.values():
                if (huber.coord == h.coord):
                    raise ValueError("Hub is already at the same coordinates "
                                     "\n"
                                     f"{name}: {coord} == {h.name}: {h.coord}")

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
            print(*line, meta)
            exit()

# ========================= CREATE END HUB ====================================

    def create_end_hub(self, line: list[Any], meta: str) -> None:
        """Create the destination hub from parsed map tokens.

        Args:
            line: Tokenized end hub definition containing name, x, and y.
            meta: Raw metadata string attached to the end hub.

        Returns:
            None.
        """
        if (len(line) != 3):
            raise ValueError(f"incorrect format {line} {meta}")

        try:

            name: str = str(line[0])
            coord: tuple[int, int] = (int(line[1]), int(line[2]))

            if (coord[0] > 100 or coord[1] > 100):
                raise ValueError("It is not possible to enter coordinates "
                                 f"greater than 100. \n{name}: {coord}")

            if not (self.hub.get(name) is None and self.end_hub is None):
                raise ValueError("end_hub duplicate")

            huber: Hub = Hub(name, coord)

            meta_dict: dict[str, Any] = self.clean_meta(meta)

            if (meta_dict):
                for k, v in meta_dict.items():
                    if (v == "blocked"):
                        raise ValueError("end_hub cannot be blocked")
                    if (k == "zone"):
                        print(f"{redp}end_hub will not take the zone change "
                              f"into account{reset}")
                    setattr(huber, k, v)

            for h in self.hub.values():
                if (huber.coord == h.coord):
                    raise ValueError("Hub is already at the same coordinates "
                                     "\n"
                                     f"{name}: {coord} == {h.name}: {h.coord}")

            huber.zone = "end"
            self.end_hub = huber
            self.hub[huber.name] = huber

            if (self.end_hub.max_drones == 1):
                self.end_hub.max_drones = self.nbr_drones

        except (ValueError, TypeError) as e:
            print(f"{red}[ERROR]{reset} : ", e)
            print(*line, meta)
            exit()

# =========================== CREATE HUB ======================================

    def create_hub(self, line: list[Any], meta: str) -> None:
        """Create a regular hub and apply validated metadata to it.

        Args:
            line: Tokenized hub definition containing name, x, and y.
            meta: Raw metadata string attached to the hub.

        Returns:
            None.
        """
        if (len(line) != 3):
            raise ValueError(f"incorrect format {line} {meta}")

        try:

            name: str = str(line[0])
            coord: tuple[int, int] = (int(line[1]), int(line[2]))

            if (coord[0] > 100 or coord[1] > 100):
                raise ValueError("It is not possible to enter coordinates "
                                 f"greater than 100. \n{name}: {coord}")

            if not (self.hub.get(name) is None):
                raise ValueError("Hub duplicate")

            huber = Hub(name, coord)

            meta_dict: dict[str, Any] = self.clean_meta(meta)

            if (meta_dict):
                for k, v in meta_dict.items():
                    setattr(huber, k, v)

            for h in self.hub.values():
                if (huber.coord == h.coord):
                    raise ValueError("Hub is already at the same coordinates "
                                     "\n"
                                     f"{name}: {coord} == {h.name}: {h.coord}")

            self.hub[huber.name] = huber

        except (ValueError, TypeError) as e:
            print(f"{red}[ERROR]{reset} : ", e)
            print(*line, meta)
            exit()

# ===================== CLEAN META CONNECTION =================================

    def clean_meta_connection(self, meta: str) -> int:
        """Extract a connection capacity from a raw metadata string.

        Args:
            meta: Raw metadata string attached to a connection.

        Returns:
            Parsed capacity, or -1 when no valid capacity metadata exists.
        """
        try:
            if (meta == ""):
                return (-1)

            if not (meta.startswith("[") and meta.endswith("]")):
                raise ValueError("The metadata is incorrect; it should be "
                                 "[max_link_capacity=positive_int]")

            if (meta[:meta.find("=")] != "[max_link_capacity"):
                raise ValueError("The connection metadata must not differ from"
                                 " `max_link_capacity`")

            nbr = int(meta[meta.find("=") + 1: - 1])

            if (nbr < 1):
                raise ValueError("max_link_capacity must be "
                                 "a positive integer")

            if (nbr > self.nbr_drones):
                raise ValueError("max_link_capacity must be less than or "
                                 "equal to the number of drones")

            return (int(meta[meta.find("=") + 1: - 1]))

        except ValueError as e:
            print(f"{red}[ERROR]{reset} : {e}")
            print(meta)
            exit()
# ========================== MAKE CONNECTION ==================================

    def make_connection(self, line: list[Any]) -> None:
        """Create and register a connection between two existing hubs.

        Args:
            line: Parsed connection tokens, with an optional metadata token.

        Returns:
            None.
        """

        try:

            if (len(line) > 2 or len(line) < 1):
                raise ValueError("data entry error ")

            meta = -1
            meta_link: int = -1
            link = line[0].split("-")

            if (len(link) != 2):
                raise ValueError("The connection is not configured correctly"
                                 "\n" + f" {line[0]} must be -> "
                                 "connection1-connection2")
            if (len(line) == 2):
                meta = line[1]
                meta_link = self.clean_meta_connection(meta)

            way_1: str = link[0]
            way_2: str = link[1]

            if (way_1 == way_2):
                raise ValueError("The connections must be different "
                                 f"({way_1}-{way_2})")

            if not (self.hub[way_1] or self.hub[way_2]):
                raise ValueError("The connection cannot be established; "
                                 f"hub is missing ({way_1} or {way_2})")

            connect: Connection = Connection(way_1, way_2)

            if (meta_link > 1):
                connect.max_link_capacity = meta_link

            for c in self.hub[way_1].connection:
                if (c.way_1 == way_1 and c.way_2 == way_2
                        or c.way_2 == way_1 and c.way_2 == way_1):
                    raise ValueError("Duplicate connection")
            self.hub[way_1].connection.append(connect)
            self.hub[way_2].connection.append(connect)

        except ValueError as e:
            print(f"{red}[ERROR]{reset} : ", e)
            print(*line)
            exit()
        except TypeError:
            print(f"{red}[ERROR]{reset} : Invalid connection;"
                  f" hub not recognized {line}")
            exit()
        except (NameError, KeyError) as e:
            print(f"{red}[ERROR]{reset} : Unknown connection {line[0]} -> {e}")
            exit()
