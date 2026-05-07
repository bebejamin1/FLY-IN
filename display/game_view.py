#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   game_view.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/20 10:45:00 by bbeaurai            #+#    #+#            #
#   Updated: 2026/05/05 10:22:18 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# python3 -m venv venv
# source venv/bin/activate

from typing import TypeAlias, cast

import arcade
from arcade.types import RGBOrA255
from parsing.parser import Level
from parsing.plateform import Hub
from display.round_manager import RoundManager

WINDOWS_WIDTH = 1920
WINDOWS_HEIGHT = 1080
WINDOWS_TITLE = "FLY-IN"

GRID_SIZE = 150
OFFSET_X = 25
OFFSET_Y = 25

MIN_ZOOM = 0.5
MAX_ZOOM = 7.00

Point: TypeAlias = tuple[int, int]
ConnectionLine: TypeAlias = tuple[Point, Point, int]


class GameView(arcade.Window):

    def __init__(self, level: Level) -> None:

        super().__init__(WINDOWS_WIDTH, WINDOWS_HEIGHT, WINDOWS_TITLE,
                         fullscreen=False)

        self.level = level
        self.background: arcade.Texture | None = None
        self.hub_textures: dict[str, arcade.Texture] = {}
        self.hub_sprites: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )
        self.drone_sprites: dict[int, arcade.Sprite] = {}
        self.drone_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.connection_lines: list[ConnectionLine] = []
        self.round_manager: RoundManager | None = None
        self.drone_texture: arcade.Texture | None = None

        self.zoom = 1.0
        self.pan_x: float = 0.0
        self.pan_y: float = 0.0
        self.panning = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.current_round = 0

        self.is_paused = True

        self.round_speed_seconds = 1.0
        self.time_since_last_round = 0.0

        self.map_min_x: float = 0.0
        self.map_max_x: float = WINDOWS_WIDTH
        self.map_min_y: float = 0.0
        self.map_max_y: float = WINDOWS_HEIGHT

        self.color_map: dict[str, RGBOrA255] = {
            "red": arcade.color.RED,
            "blue": arcade.color.BLUE,
            "green": arcade.color.GREEN,
            "yellow": arcade.color.YELLOW,
            "orange": arcade.color.ORANGE,
            "purple": arcade.color.PURPLE,
            "cyan": arcade.color.CYAN,
            "lime": arcade.color.LIME,
            "violet": arcade.color.VIOLET,
            "black": arcade.color.BLACK,
            "white": arcade.color.BLACK,
            "brown": (139, 69, 19),
            "gold": arcade.color.GOLD,
            "maroon": arcade.color.MAROON,
            "crimson": arcade.color.CRIMSON,
            "rainbow": arcade.color.WHITE,
            "darkred": (139, 0, 0),
            "salmon": (219, 151, 230)
        }

# *****************************************************************************
# *                               setup                                       *
# *                                                                           *

    def setup(self) -> None:
        self.background = arcade.load_texture(
            "display/resources/background.jpg"
                                             )

        self.hub_textures = {
            "start": arcade.load_texture("display/resources/START.png"),
            "end": arcade.load_texture("display/resources/END.png"),
            "normal": arcade.load_texture("display/resources/NORMAL.png"),
            "blocked": arcade.load_texture("display/resources/BLOCKED.png"),
            "restricted": arcade.load_texture(
                "display/resources/RESTRICTED.png"
            ),
            "priority": arcade.load_texture("display/resources/PRIORITY.png"),
                           }

        for hub in self.level.hub.values():
            texture = self.hub_textures.get(
                hub.zone, self.hub_textures["normal"]
                                           )
            sprite = arcade.Sprite(texture)

            sprite.scale = 0.05
            sprite.center_x = hub.coord[0] * GRID_SIZE + OFFSET_X
            sprite.center_y = hub.coord[1] * GRID_SIZE + OFFSET_Y
            self.hub_sprites.append(sprite)

        drawn_connections: set[tuple[str, str]] = set()
        for hub in self.level.hub.values():
            for conn in hub.connection:
                way_1, way_2 = sorted((conn.way_1, conn.way_2))
                conn_key = (way_1, way_2)
                if conn_key in drawn_connections:
                    continue
                drawn_connections.add(conn_key)

                hub1 = self.level.hub[conn.way_1]
                hub2 = self.level.hub[conn.way_2]
                x1 = hub1.coord[0] * GRID_SIZE + OFFSET_X
                y1 = hub1.coord[1] * GRID_SIZE + OFFSET_Y
                x2 = hub2.coord[0] * GRID_SIZE + OFFSET_X
                y2 = hub2.coord[1] * GRID_SIZE + OFFSET_Y
                self.connection_lines.append(
                    ((x1, y1), (x2, y2), conn.max_link_capacity)
                )

        self.round_manager = RoundManager(self.level)

        self.drone_texture = arcade.load_texture("display"
                                                 "/resources/drone1.gif")

        for i in range(self.level.nbr_drones):
            sprite = arcade.Sprite(self.drone_texture)
            sprite.scale = 0.05
            if self.level.start_hub:
                sprite.center_x = (
                    self.level.start_hub.coord[0] * GRID_SIZE + OFFSET_X
                )
                sprite.center_y = (
                    self.level.start_hub.coord[1] * GRID_SIZE + OFFSET_Y
                )
            self.drone_sprites[i] = sprite
            self.drone_list.append(sprite)

        self._center_map()

# *****************************************************************************
# *                               Center                                      *
# *                                                                           *

    def _center_map(self) -> None:
        if not self.level.hub:
            return

        coords = [hub.coord for hub in self.level.hub.values()]
        min_x = min(c[0] for c in coords)
        max_x = max(c[0] for c in coords)
        min_y = min(c[1] for c in coords)
        max_y = max(c[1] for c in coords)

        self.map_min_x = (min_x - 2) * GRID_SIZE + OFFSET_X
        self.map_max_x = (max_x + 2) * GRID_SIZE + OFFSET_X
        self.map_min_y = (min_y - 2) * GRID_SIZE + OFFSET_Y
        self.map_max_y = (max_y + 2) * GRID_SIZE + OFFSET_Y

        center_x = ((min_x + max_x) / 2) * GRID_SIZE + OFFSET_X
        center_y = ((min_y + max_y) / 2) * GRID_SIZE + OFFSET_Y

        self.zoom = 1.0

        self.pan_x = center_x
        self.pan_y = center_y

# *****************************************************************************
# *                               Draw                                        *
# *                                                                           *

    def on_draw(self) -> None:

        background = self.background
        if background is not None:
            arcade.draw_texture_rect(
                background,
                arcade.LBWH(0, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
            )
        else:
            self.clear(arcade.color.DARK_BLUE_GRAY)

        screen_x = WINDOWS_WIDTH / 2 - self.pan_x * self.zoom
        screen_y = WINDOWS_HEIGHT / 2 - self.pan_y * self.zoom

        for (start, end, capacity) in self.connection_lines:
            x1 = screen_x + start[0] * self.zoom
            y1 = screen_y + start[1] * self.zoom
            x2 = screen_x + end[0] * self.zoom
            y2 = screen_y + end[1] * self.zoom
            arcade.draw_line(
                int(x1), int(y1), int(x2), int(y2), arcade.color.BROWN, 4
                            )
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            arcade.draw_text(
                str(capacity), int(mid_x), int(mid_y),
                arcade.color.BLACK, max(6, int(10 * self.zoom)),
                anchor_x="center"
                            )

        for i, hub_sprite in enumerate(self.hub_sprites):
            hub = list(self.level.hub.values())[i]

            hub_sprite.center_x = (
                screen_x + (hub.coord[0] * GRID_SIZE + OFFSET_X) * self.zoom
                                  )
            hub_sprite.center_y = (
                screen_y + (hub.coord[1] * GRID_SIZE + OFFSET_Y) * self.zoom
                                  )

            hub_sprite.scale = 0.06 * self.zoom

        self.hub_sprites.draw()

        for hub in self.level.hub.values():

            world_x = hub.coord[0] * GRID_SIZE + OFFSET_X
            world_y = hub.coord[1] * GRID_SIZE + OFFSET_Y

            x = screen_x + world_x * self.zoom
            y = screen_y + world_y * self.zoom

            rect_color: RGBOrA255 = arcade.color.BLACK
            if hub.color and hub.color.lower() != "white":
                rect_color = self.color_map.get(hub.color.lower(),
                                                arcade.color.BLACK)

            rect_width = len(hub.name) * 11 * self.zoom
            rect_height = 16 * self.zoom

            rect_y_center = y + (40 * self.zoom) + (rect_height / 2)

            arcade.draw_rect_filled(
                arcade.XYWH(int(x), int(rect_y_center), int(rect_width),
                            int(rect_height)),
                rect_color
            )

            arcade.draw_text(
                hub.name,
                int(x),
                int(y + (40 * self.zoom)),
                arcade.color.WHITE,
                max(6, int(10 * self.zoom)),
                anchor_x="center",
                anchor_y="bottom"
            )

            arcade.draw_text(
                f"Drone {hub.current}/{hub.max_drones}",
                int(x),
                int(y - (35 * self.zoom)),
                arcade.color.RED,
                max(4, int(8 * self.zoom)),
                anchor_x="center",
                anchor_y="top"
            )

            arcade.draw_text(
                f"Cost:{hub.value}",
                int(x),
                int(y - (50 * self.zoom)),
                arcade.color.RED,
                max(4, int(8 * self.zoom)),
                anchor_x="center",
                anchor_y="top"
            )

        self.drone_list.draw()

        pause_text = "PAUSED" if self.is_paused else "RUNNING"

        round_manager = cast(RoundManager, self.round_manager)
        end_hub = cast(Hub, self.level.end_hub)

        status_text = (
            f"Round: {round_manager.current_round}\n"
            f"Status: {pause_text}\n"
            f"Speed: {self.round_speed_seconds:.1f}s / round\n"
            f"Completed drones {end_hub.current}/"
            f"{self.level.nbr_drones}"
        )

        arcade.draw_text(
            status_text, 20, self.height - 20,
            arcade.color.WHITE, 14,
            anchor_x="left", anchor_y="top", multiline=True, width=300
        )

        controls_text = (
            "--- CONTROLS ---\n"
            "[SPACE] : Play / Pause\n"
            "[ + ] : Speed Up\n"
            "[ - ] : Speed Down\n"
            "[ R ] : Reset Simulation\n"
            "[ Q ] : Quit Simulation\n"
            "[Mouse] : Pan & Scroll"
        )

        arcade.draw_text(
            controls_text, 20, 20,
            arcade.color.BLACK, 12,
            anchor_x="left", anchor_y="bottom",
            multiline=True, width=300, align="left"
        )

        if end_hub.current == self.level.nbr_drones:

            self.is_paused = True

            arcade.draw_rect_filled(
                arcade.XYWH(self.width / 2, self.height / 2, self.width,
                            self.height), (0, 0, 0, 180)
                                    )

            arcade.draw_text(
                "FINISH",
                self.width / 2, self.height / 2 + 30,
                arcade.color.GOLD,
                80,
                anchor_x="center", anchor_y="center", bold=True
            )

            arcade.draw_text(
                "Press [ R ] to Restart or [ Q ] to Quit",
                self.width / 2, self.height / 2 - 50,
                arcade.color.WHITE,
                20,
                anchor_x="center", anchor_y="center"
            )

# *****************************************************************************
# *                               Round                                       *
# *                                                                           *

    def next_round(self) -> None:
        if self.round_manager:

            logs = self.round_manager.execute_round()

            if logs:
                print(" ".join(logs))

# *****************************************************************************
# *                              Animate                                      *
# *                                                                           *

    def on_update(self, delta_time: float) -> None:

        if not self.round_manager:
            return

        round_manager = self.round_manager

        if not self.is_paused:
            self.time_since_last_round += delta_time

            if self.time_since_last_round >= self.round_speed_seconds:
                self.next_round()
                self.time_since_last_round = 0.0

        screen_x = self.width / 2 - self.pan_x * self.zoom
        screen_y = self.height / 2 - self.pan_y * self.zoom
        ANIMATION_SPEED = 8.0

        for drone_id, drone_sprite in self.drone_sprites.items():
            drone_key = f"drone{drone_id}"
            if drone_key not in round_manager.drones:
                continue
            drone = round_manager.drones[drone_key]

            if drone.hub_current == "IN_TRANSIT":
                source_hub = self.level.hub[cast(str, drone.transit_source)]
                dest_hub = self.level.hub[
                    cast(str, drone.transit_destination)
                ]
                world_x = (source_hub.coord[0] + dest_hub.coord[0]) / 2
                world_y = (source_hub.coord[1] + dest_hub.coord[1]) / 2
            else:
                hub = self.level.hub[drone.hub_current]
                world_x = hub.coord[0]
                world_y = hub.coord[1]

            target_x = screen_x + (world_x * GRID_SIZE + OFFSET_X) * self.zoom
            target_y = screen_y + (world_y * GRID_SIZE + OFFSET_Y) * self.zoom

            drone_sprite.center_x += (target_x - drone_sprite.center_x)\
                * ANIMATION_SPEED * delta_time
            drone_sprite.center_y += (target_y - drone_sprite.center_y)\
                * ANIMATION_SPEED * delta_time
            drone_sprite.scale = 0.08 * self.zoom

# *****************************************************************************
# *                               Clamp                                       *
# *                                                                           *

    def _clamp_pan(self) -> None:
        visible_width = WINDOWS_WIDTH / self.zoom
        visible_height = WINDOWS_HEIGHT / self.zoom

        self.pan_x = max(
            self.map_min_x + visible_width / 2,
            min(self.pan_x, self.map_max_x - visible_width / 2)
                        )
        self.pan_y = max(
            self.map_min_y + visible_height / 2,
            min(self.pan_y, self.map_max_y - visible_height / 2)
                        )

# *****************************************************************************
# *                               Mouv                                        *
# *                                                                           *

    def on_mouse_press(
        self, x: int, y: int, button: int, modifiers: int
                      ) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.panning = True
            self.last_mouse_x = x
            self.last_mouse_y = y

    def on_mouse_release(
        self, x: int, y: int, button: int, modifiers: int
                        ) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.panning = False

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        if self.panning:

            self.pan_x -= dx / self.zoom
            self.pan_y -= dy / self.zoom
            self._clamp_pan()

    def on_mouse_scroll(
        self, x: int, y: int, scroll_x: float, scroll_y: float
    ) -> None:

        zoom_factor = 1.15
        if scroll_y > 0:
            self.zoom *= zoom_factor
        elif scroll_y < 0:
            self.zoom /= zoom_factor

        self.zoom = max(MIN_ZOOM, min(MAX_ZOOM, self.zoom))

        self._clamp_pan()

    def on_key_press(self, key: int, modifiers: int) -> None:

        if key == arcade.key.Q:
            self.close()

        elif key == arcade.key.SPACE:
            self.is_paused = not self.is_paused

        elif key == arcade.key.R:
            if self.round_manager:
                self.round_manager.reset()
                self.current_round = 0
                self.time_since_last_round = 0.0
                self.is_paused = True

        elif key == arcade.key.PLUS or key == arcade.key.NUM_ADD\
                or key == arcade.key.EQUAL:
            self.round_speed_seconds = max(0.1, self.round_speed_seconds - 0.2)

        elif key == arcade.key.MINUS or key == arcade.key.NUM_SUBTRACT:
            self.round_speed_seconds = min(5.0, self.round_speed_seconds + 0.2)


def main(level: Level) -> None:
    windows = GameView(level)
    windows.setup()
    arcade.run()


if __name__ == "__main__":
    level = Level()
    level.nbr_drones = 2

    hub1 = Hub("start", (0, 0))
    hub1.zone = "start"
    level.start_hub = hub1
    level.hub["start"] = hub1
    hub2 = Hub("end", (5, 5))
    hub2.zone = "end"
    level.end_hub = hub2
    level.hub["end"] = hub2
    main(level)
