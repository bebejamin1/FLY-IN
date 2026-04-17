#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/07 11:00:13 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/17 17:58:08 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import sys
import random

from pathlib import Path

from parsing.map_parser import MapParser


green = "\033[32m\033[1m\033[1m"
red = "\033[31m\033[5m\033[1m"
redp = "\033[31m"
brown = "\033[0;33m"
blue = "\033[38;5;67m"
reset = "\033[0m"


class MapSelector:

    def __init__(self) -> None:
        self.directory: Path = Path("maps")
        print(self.directory)

    def display_file(self) -> None:
        ran = random.randint(55, 60)
        print(blue)
        print("  _.--._  _.--._".center(ran, " "))
        print(",-=.-\":;:;:;\':;:;:;\"-._".center(ran, " "))
        print("\\\\:;:;:;:;:;\\:;:;:;:;:;\\".center(ran, " "))
        print(" \\\\:;:;:;:;:;\\:;:;:;:;:;\\".center(ran, " "))
        print("  \\\\:;:;:;:;:;\\:;:;:;:;:;\\".center(ran, " "))
        print("   \\\\:;:;:;:;:;\\:;::;:;:;:\\".center(ran, " "))
        print("    \\\\;:;::;:;:;\\:;:;:;::;:\\".center(ran, " "))
        print("     \\\\;;:;:_:--:\\:_:--:_;:;\\".center(ran, " "))
        print("      \\\\_.-\"      :      \"-._\\".center(ran, " "))
        print("       \\`_..--""--.;.--\"\"--.._=>".center(ran, " "))
        print("        \"".center(ran, " "))
        print(reset)

    def display_level(self) -> None:
        print(blue)
        print("     ----.".center(60, " "))
        print("    \"   _}".center(60, " "))
        print("    \"@   >".center(60, " "))
        print("    |\\   7".center(60, " "))
        print("    / `-- _         ,-------,****".center(60, " "))
        print(" ~    >o<  \\---------o{___}-".center(60, " "))
        print("/  |  \\  /  ________/8'".center(60, " "))
        print("|  |       /         \"".center(60, " "))
        print("|  /      |".center(60, " "))
        print("")
        print(reset)

# *****************************************************************************
# *                               files                                       *
# *                                                                           *

    def get_available_file(self) -> list[Path]:

        return (list(self.directory.rglob("")))

    def get_available_level(self, map_file: str) -> list[Path]:

        folder = Path(map_file)

        if not folder.exists() or not folder.is_dir():
            return []

        return sorted(folder.glob("*.txt"))

    def prompt_user(self) -> Path | None:
        files: list[Path] = self.get_available_file()

        if (not files):
            print(f"{red}[ERROR]{reset} No files found in the folder"
                  f"'{self.directory.name}'.")
            return (None)
        del files[0]

        try:

            while (True):

                os.system('clear')

                self.display_file()

                print("\n" + "🗂️  Available files :" + "\n")
                for i, file_path in enumerate(files):
                    print(f"  {blue}[{i + 1}]{brown} {file_path.name}{reset}")

                print("\n" + f"  {redp}[{len(files) + 1}] Exit{reset}")

                choice_file: str = input("\nSelect a file "
                                         f"(1-{len(files) + 1}) : ")

                if (choice_file.isdigit()):

                    if (int(choice_file) == len(files) + 1):
                        sys.exit()

                index: int = int(choice_file) - 1

                if (0 <= index < len(files)):
                    map_files: Path = files[index]
                    break

                print(f"{red}[ERROR]{reset} Invalid. Try again.")

            levels: list[Path] = self.get_available_level(map_files)

            if not levels:
                print(f"{red}[ERROR]{reset} No map (.txt) found "
                      f"in the folder '{self.directory.name}'.")
                return (None)

            while (True):

                os.system('clear')

                self.display_level()

                print("\n" + "🗺️ Available maps :" + "\n")
                for i, file_path in enumerate(levels):
                    print(f"  {blue}[{i + 1}]{brown} {file_path.name}{reset}")

                print("\n" + f"  {redp}[{len(levels) + 1}] Back{reset}")

                choise_level: str = input("\nChoose a level "
                                          f"(1-{len(levels) + 1}) : ")

                if choise_level.isdigit():
                    if (int(choise_level) == (len(levels) + 1)):
                        self.prompt_user()

                    index: int = int(choise_level) - 1

                if 0 <= index < len(levels):
                    level: Path = levels[index]
                    return (level)

                print(f"{red}[ERROR]{reset} Invalid. Try again.")

        except (UnboundLocalError, AttributeError, KeyboardInterrupt):
            print("gepoghnep")

        return (None)

# *****************************************************************************
# *                                main                                       *
# *                                                                           *


def main() -> None:

    try:

        selector = MapSelector()

        map_level: Path | None = selector.prompt_user()
        print(map_level)

        if (map_level is None):
            raise AttributeError("Program stopped")

        level_load: MapParser | None = MapParser(map_level).parse_maps()

        print(level_load)

        # for k, v in level_load.hub.items():
        #     print(k)
        #     for connect in v.connection:
        #         print(connect.way_1, connect.way_2, "\n")

        # parsing fini commence a soit cree laffichage soit cree lalgo
        # revoir la maniere de stockage des connections

    except (KeyboardInterrupt, UnboundLocalError, AttributeError):
        print("Program canceled")


if __name__ == "__main__":
    main()
