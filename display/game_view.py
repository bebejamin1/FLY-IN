#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   game_view.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/20 10:45:00 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/20 14:37:29 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# python3 -m venv venv
# source venv/bin/activate

import arcade

WINDOWS_WIDTH = 1280
WINDOWS_HEIGHT = 720
WINDOWS_TITLE = "FLY-IN"


class GameView(arcade.Window):

    def __init__(self) -> None:

        super().__init__(WINDOWS_WIDTH, WINDOWS_HEIGHT, WINDOWS_TITLE)

        self.background = None

    def setup(self) -> None:
        self.background = arcade.load_texture("../display/resources/background.jpg")

    def on_draw(self) -> None:
        self.clear

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            WINDOWS_WIDTH, WINDOWS_HEIGHT,
                                            self.background)


def main():
    windows = GameView()
    windows.setup()
    arcade.run()


if __name__ == "__main__":
    main()
