#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/07 11:00:13 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/07 17:12:42 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import os
import sys
import random

from pathlib import Path


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
        print("                   __-----_.           "
              "             ______".center(60, " "))
        print("          /  \\      \\           o  O "
              " O   _(      )__".center(60, " "))
        print("         /    |  |   \\_---_   o._.    "
              "  _(           )_".center(60, " "))
        print("        |     |            \\   | |\"\""
              "\"\"(_   Let's see... )".center(60, " "))
        print("        |     |             |@ | |    ("
              "_               _)".center(60, " "))
        print("         \\___/   ___       /   | |    "
              "  (__          _)".center(60, " "))
        print("           \\____(____\\___/     | |   "
              "      (________)".center(60, " "))
        print("           |__|                | |     "
              "     |".center(60, " "))
        print("           /   \\-_             | |    "
              "     |'".center(60, " "))
        print("         /      \\_ \"__ _       !_!--v"
              "---v--\"".center(60, " "))
        print("        /         \"|  |>)      |\"\"\""
              "\"\"\"\"\"|".center(60, " "))
        print("       |          _|  | ._--""||       "
              " |".center(60, " "))
        print("       _\\_____________|_|_____||______"
              "__|_".center(60, " "))
        print("      /                                "
              "   \\".center(60, " "))
        print("     /_________________________________"
              "____\\".center(60, " "))
        print("     /                                 "
              "    \\".center(60, " "))
        print("    /__________________________________"
              "_____\\".center(60, " "))
        print("    /                                  "
              "     \\".center(60, " "))
        print("   /___________________________________"
              "______\\".center(60, " "))
        print("        {                              "
              " }".center(60, " "))
        print("        <______________________________"
              "_|".center(60, " "))
        print("        |                              "
              " >".center(60, " "))
        print("        {______________________________"
              "_|               ________".center(60, " "))
        print("        <                              "
              " }              / SNOOPY \\".center(60, " "))
        print("        |______________________________"
              "_|             /__________\\".center(60, " "))
        print("\\|/       \\\\/             \\||//    "
              "       |//                       \\|/    |/".center(60, " "))
        print(reset)

# *****************************************************************************
# *                               files                                       *
# *                                                                           *

    def get_available_file(self) -> list[Path]:

        return (list(self.directory.rglob("")))

    def prompt_user_file(self) -> Path | None:
        files: list[Path] = self.get_available_file()

        if (not files):
            print(f"{red}[ERROR]{reset} No files found in the folder"
                  f"'{self.directory.name}'.")
            return (None)
        del files[0]

        while (True):

            try:

                # os.system('clear')

                self.display_file()

                print("\n" + "🗂️  Available files :" + "\n")
                for i, file_path in enumerate(files):
                    print(f"  {blue}[{i + 1}]{brown} {file_path.name}{reset}")

                print("\n" + f"  {redp}[{len(files) + 1}] Exit{reset}")

                choice_file: str = input("\nSelect a file "
                                         f"(1-{len(files) + 1}) : ")
                print(int(choice_file) == {len(files) + 1})
                if (choice_file.isdigit()):

                    if (int(choice_file) == {len(files) + 1}):
                        sys.exit()

                index: int = int(choice_file) - 1

                if (0 <= index < len(files)):
                    file: Path = files[index]
                    return (file)

                print(f"{red}[ERROR]{reset} Invalid. Try again.")

            except (UnboundLocalError, AttributeError):
                print("gepoghnep")
        return (None)

# *****************************************************************************
# *                                level                                      *
# *                                                                           *

    def get_available_level(self, map_file: str) -> list[Path]:

        folder = Path(map_file)

        if not folder.exists() or not folder.is_dir():
            return []

        return sorted(folder.glob("*.txt"))

    def prompt_user_level(self, map_file: str) -> Path | None:

        levels: list[Path] = self.get_available_level(map_file)

        if not levels:
            print(f"{red}[ERROR]{reset} No map (.txt) found in the folder "
                  f"'{self.directory.name}'.")
            return (None)

        while (True):
            try:

                # os.system('clear')

                self.display_level()

                print("\n" + "🗺️ Available maps :" + "\n")
                for i, file_path in enumerate(levels):
                    print(f"  {blue}[{i + 1}]{brown} {file_path.name}{reset}")

                print("\n" + f"  {redp}[{len(levels) + 1}] Back{reset}")

                choise_level: str = input("\nChoose a level "
                                          f"(1-{len(levels) + 1}) : ")

                if choise_level.isdigit():
                    print(choise_level)
                    print(len(levels))
                    if (choise_level == (len(levels) + 1)):
                        self.prompt_user_file()

                    index: int = int(choise_level) - 1

                if 0 <= index < len(levels):
                    level: Path = levels[index]
                    return (level)

                print(f"{red}[ERROR]{reset} Invalid. Try again.")

            except (UnboundLocalError):
                print("gekogp")


def main() -> None:

    try:

        selector = MapSelector()

        map_file: Path | None = selector.prompt_user_file()

        if (map_file is None):
            raise AttributeError("Program stopped")

        print(map_file)
        map_level: Path | None = selector.prompt_user_level(map_file)

    except (KeyboardInterrupt, UnboundLocalError):
        print("Program canceled")

    print(map_level)


if __name__ == "__main__":
    main()
