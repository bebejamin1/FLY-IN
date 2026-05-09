#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/07 11:00:13 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/01 13:21:36 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Command-line entry point for selecting, solving, and displaying a map."""

import os
import sys
import random

from pathlib import Path

from parsing.map_parser import MapParser
from parsing.parser import Level
from display.game_view import main as display_main
from algorithm.dijkstra import Algorithm
from algorithm.path_checker import PathChecker


green = "\033[32m\033[1m\033[1m"
red = "\033[31m\033[5m\033[1m"
redp = "\033[31m"
brown = "\033[0;33m"
blue = "\033[38;5;67m"
reset = "\033[0m"


class MapSelector:
    """Handle interactive selection of map folders and level files.

    Attributes:
        directory: Root folder where map packs are searched.
    """

    def __init__(self) -> None:
        """Initialize the selector with the default maps directory.

        Returns:
            None.
        """
        self.directory: Path = Path("maps")
        print(self.directory)

    def display_file(self) -> None:
        """Print the ASCII banner used on the map-folder selection screen.

        Returns:
            None.
        """
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
        """Print the ASCII banner used on the level selection screen.

        Returns:
            None.
        """
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
        """List the available map pack folders from the maps directory.

        Returns:
            Paths found below the configured maps directory.
        """
        return (list(self.directory.rglob("")))

    def get_available_level(self, map_file: str | Path) -> list[Path]:
        """List playable map files inside a selected map pack folder.

        Args:
            map_file: Directory path selected by the user.

        Returns:
            Sorted list of text files found in the selected directory.
        """
        folder = Path(map_file)

        if not folder.exists() or not folder.is_dir():
            return []

        return sorted(folder.glob("*.txt"))

    def prompt_user(self) -> Path | None:
        """Prompt the user to choose a map pack and level file.

        Returns:
            Selected map file path, or None when selection cannot continue.
        """
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

                if (not choice_file.isdigit()):
                    print(f"{red}[ERROR]{reset} Invalid. Try again.")
                    continue

                choice_file_index: int = int(choice_file)

                if (choice_file_index == len(files) + 1):
                    sys.exit()

                index_file: int = choice_file_index - 1

                if (0 <= index_file < len(files)):
                    map_files: Path = files[index_file]
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

                if (not choise_level.isdigit()):
                    print(f"{red}[ERROR]{reset} Invalid. Try again.")
                    continue

                choise_level_index: int = int(choise_level)

                if (choise_level_index == (len(levels) + 1)):
                    return (self.prompt_user())

                index_level: int = choise_level_index - 1

                if 0 <= index_level < len(levels):
                    level: Path = levels[index_level]
                    return (level)

                print(f"{red}[ERROR]{reset} Invalid. Try again.")

        except (UnboundLocalError, AttributeError, KeyboardInterrupt):
            print("  Goodbye ... ;)")
            exit()

        except ValueError:
            return (self.prompt_user())

        return (None)

# *****************************************************************************
# *                                main                                       *
# *                                                                           *


def main() -> None:
    """Run the full FLY-IN flow from map selection to graphical display.

    Returns:
        None.
    """
    try:

        selector = MapSelector()

        map_level: Path | None = selector.prompt_user()

        if (map_level is None):
            raise AttributeError("Program stopped")

        level_load: Level = MapParser(map_level).parse_maps()

        if (not PathChecker(level_load).is_path_possible()):
            raise ValueError("No possible path between start_hub and end_hub")

        level_algo: Level = Algorithm(level_load).make_algo()

        display_main(level_algo)

    except KeyboardInterrupt:
        print("Program canceled")

    except ValueError as e:
        print(f"{red}[ERROR]{reset} : {e}")

    except Exception as e:
        print("\n" + f"{red}[CRASH]{reset}")
        print(e)


if __name__ == "__main__":
    main()
