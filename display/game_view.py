#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   game_view.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bbeaurai <bbeaurai@student.42lehavre.fr>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/20 10:45:00 by bbeaurai            #+#    #+#            #
#   Updated: 2026/04/27 13:19:05 by bbeaurai           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

# python3 -m venv venv
# source venv/bin/activate

import arcade
from parsing.parser import Level
# from display.round_manager import RoundManager

WINDOWS_WIDTH = 1920
WINDOWS_HEIGHT = 1080
WINDOWS_TITLE = "FLY-IN"

GRID_SIZE = 150
OFFSET_X = 25
OFFSET_Y = 25

# Camera settings
MIN_ZOOM = 0.5
MAX_ZOOM = 7.00


class GameView(arcade.Window):

    def __init__(self, level: Level) -> None:

        super().__init__(WINDOWS_WIDTH, WINDOWS_HEIGHT, WINDOWS_TITLE)

        self.level = level
        self.background = None
        self.hub_sprites = arcade.SpriteList()
        self.drone_sprites = {}
        self.drone_list = arcade.SpriteList()
        self.connection_lines = []
        self.round_manager = None
        self.drone_texture = None

        # Camera and pan settings
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.panning = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0

        # Round management
        self.current_round = 0
        self.is_paused = False
        self.round_speed = 2  # Nombre de frames avant le prochain round
        self.frame_counter = 0

        # Map boundaries
        self.map_min_x = 0
        self.map_max_x = WINDOWS_WIDTH
        self.map_min_y = 0
        self.map_max_y = WINDOWS_HEIGHT

        # Color map for hubs
        self.color_map = {
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
            "brown": (139, 69, 19),
            "gold": arcade.color.GOLD,
            "maroon": arcade.color.MAROON,
            "crimson": arcade.color.CRIMSON,
            "rainbow": arcade.color.WHITE,
            "darkred": (139, 0, 0),
        }

# *****************************************************************************
# *                               setup                                       *
# *                                                                           *

    def setup(self) -> None:
        self.background = arcade.load_texture(
            "display/resources/background.jpg"
                                             )

        # Load hub textures
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
            # Set uniform scale for all hubs
            sprite.scale = 0.05
            sprite.center_x = hub.coord[0] * GRID_SIZE + OFFSET_X
            sprite.center_y = hub.coord[1] * GRID_SIZE + OFFSET_Y
            self.hub_sprites.append(sprite)

        # Create connection lines
        drawn_connections = set()
        for hub in self.level.hub.values():
            for conn in hub.connection:
                conn_key = tuple(sorted([conn.way_1, conn.way_2]))
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

        # Create round manager and drones
        # self.round_manager = RoundManager(
        #     self.level.nbr_drones,
        #     self.level.start_hub.name if self.level.start_hub else "start"
        # )

        # Load drone texture
        self.drone_texture = arcade.load_texture("display"
                                                 "/resources/drone1.gif")

        # Create sprite for each drone
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

        # Auto-center the map
        self._center_map()

# *****************************************************************************
# *                               Center                                      *
# *                                                                           *

    def _center_map(self) -> None:
        if not self.level.hub:
            return

        # Calculate bounds
        coords = [hub.coord for hub in self.level.hub.values()]
        min_x = min(c[0] for c in coords)
        max_x = max(c[0] for c in coords)
        min_y = min(c[1] for c in coords)
        max_y = max(c[1] for c in coords)

        # Store map boundaries for pan limiting (in world coordinates)
        self.map_min_x = (min_x - 2) * GRID_SIZE + OFFSET_X
        self.map_max_x = (max_x + 2) * GRID_SIZE + OFFSET_X
        self.map_min_y = (min_y - 2) * GRID_SIZE + OFFSET_Y
        self.map_max_y = (max_y + 2) * GRID_SIZE + OFFSET_Y

        # Calculate center of the hub structure
        center_x = ((min_x + max_x) / 2) * GRID_SIZE + OFFSET_X
        center_y = ((min_y + max_y) / 2) * GRID_SIZE + OFFSET_Y

        # Set initial zoom to a reasonable level
        self.zoom = 1.0

        # Center the structure at the screen center
        self.pan_x = center_x
        self.pan_y = center_y

# *****************************************************************************
# *                               Draw                                        *
# *                                                                           *

    def on_draw(self) -> None:
        # Draw background first
        if self.background:
            arcade.draw_texture_rect(
                self.background,
                arcade.LBWH(0, 0, WINDOWS_WIDTH, WINDOWS_HEIGHT)
            )
        else:
            self.clear(arcade.color.DARK_BLUE_GRAY)

        # Calculate camera transformation
        screen_x = WINDOWS_WIDTH / 2 - self.pan_x * self.zoom
        screen_y = WINDOWS_HEIGHT / 2 - self.pan_y * self.zoom

        # Draw connections with transformation
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
                arcade.color.RED, max(6, int(10 * self.zoom)),
                anchor_x="center"
                            )

        # Draw hubs with transformation and zoom-adjusted scale
        for i, hub_sprite in enumerate(self.hub_sprites):
            hub = list(self.level.hub.values())[i]

            hub_sprite.center_x = (
                screen_x + (hub.coord[0] * GRID_SIZE + OFFSET_X) * self.zoom
                                  )
            hub_sprite.center_y = (
                screen_y + (hub.coord[1] * GRID_SIZE + OFFSET_Y) * self.zoom
                                  )

            # Adjust sprite scale based on zoom level
            hub_sprite.scale = 0.06 * self.zoom

        self.hub_sprites.draw()

        # Draw hub info (name above hub, values below)
        for hub in self.level.hub.values():
            # Calculate hub world position
            world_x = hub.coord[0] * GRID_SIZE + OFFSET_X
            world_y = hub.coord[1] * GRID_SIZE + OFFSET_Y
            # Calculate hub screen position (with zoom to follow hubs)
            x = screen_x + world_x * self.zoom
            y = screen_y + world_y * self.zoom

            # 1. Draw name ABOVE the hub
            arcade.draw_text(
                hub.name,
                int(x),
                int(y + (40 * self.zoom)),
                arcade.color.WHITE,
                max(6, int(10 * self.zoom)),
                anchor_x="center",
                anchor_y="bottom"
                           )

            # 2. Draw max_drones BELOW the hub
            arcade.draw_text(
                f"Max drones:{hub.max_drones}",
                int(x),
                int(y - (35 * self.zoom)),
                arcade.color.RED,
                max(4, int(8 * self.zoom)),
                anchor_x="center",
                anchor_y="top"
                           )

            # 3. Draw cost BELOW max_drones
            arcade.draw_text(
                f"Cost:{hub.value}",
                int(x),
                int(y - (50 * self.zoom)),
                arcade.color.RED,
                max(4, int(8 * self.zoom)),
                anchor_x="center",
                anchor_y="top"
                            )

        # Draw drones with transformation and zoom-adjusted scale
        for drone_id, drone_sprite in self.drone_sprites.items():
            if self.round_manager:
                current_hub_name = self.round_manager\
                                       .get_drone_current_hub(drone_id)
                if current_hub_name in self.level.hub:
                    hub = self.level.hub[current_hub_name]
                    drone_sprite.center_x = screen_x + (
                        hub.coord[0] * GRID_SIZE + OFFSET_X
                                                       ) * self.zoom
                    drone_sprite.center_y = screen_y + (
                        hub.coord[1] * GRID_SIZE + OFFSET_Y
                                                       ) * self.zoom
                    # Adjust drone scale based on zoom level
                    drone_sprite.scale = 0.08 * self.zoom

        self.drone_list.draw()
        # Draw round info in top-right corner
        arcade.draw_text(
            f"Round: {self.current_round}",
            WINDOWS_WIDTH - 150, WINDOWS_HEIGHT - 25,
            arcade.color.WHITE, 14
                        )

        # Draw pause status
        pause_text = "PAUSED" if self.is_paused else "RUNNING"
        pause_color = arcade.color.RED if self.is_paused\
            else arcade.color.GREEN

        arcade.draw_text(
            pause_text,
            WINDOWS_WIDTH - 150, WINDOWS_HEIGHT - 50,
            pause_color, 12
                        )

        # Draw hub count in top-left corner
        hub_count = len(self.level.hub)
        arcade.draw_text(
            f"Hubs: {hub_count}", 10, WINDOWS_HEIGHT - 25,
            arcade.color.WHITE, 14
                        )

# *****************************************************************************
# *                               Clamp                                       *
# *                                                                           *

    def _clamp_pan(self) -> None:
        visible_width = WINDOWS_WIDTH / self.zoom
        visible_height = WINDOWS_HEIGHT / self.zoom

        # Clamp pan position
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
            # Intuitive movement: moving mouse left moves view right
            self.pan_x -= dx / self.zoom
            self.pan_y -= dy / self.zoom
            self._clamp_pan()

    def on_mouse_scroll(
        self, x: int, y: int, scroll_x: int, scroll_y: int
    ) -> None:

        # Update zoom based on scroll direction
        zoom_factor = 1.15
        if scroll_y > 0:  # Scroll up = zoom in
            self.zoom *= zoom_factor
        elif scroll_y < 0:  # Scroll down = zoom out
            self.zoom /= zoom_factor

        # Clamp zoom
        self.zoom = max(MIN_ZOOM, min(MAX_ZOOM, self.zoom))

        self._clamp_pan()

    def on_key_press(self, key: int, modifiers: int) -> None:
        # SPACE: Execute round
        if key == arcade.key.SPACE:
            self.next_round()

        # P: Pause/Resume
        elif key == arcade.key.P:
            if self.is_paused:
                self.resume()
            else:
                self.pause()

        # R: Reset
        elif key == arcade.key.R:
            if self.round_manager:
                self.round_manager.reset()
                self.current_round = 0
                self.frame_counter = 0

        # +: speed
        elif key == arcade.key.PLUS or key == arcade.key.EQUAL:
            self.round_speed = max(1, self.round_speed - 1)

        # -: slow
        elif key == arcade.key.MINUS:
            self.round_speed += 1

# *****************************************************************************
# *                               Mouv                                        *
# *                                                                           *

# round manage


def main(level: Level):
    windows = GameView(level)
    windows.setup()
    arcade.run()


if __name__ == "__main__":
    level = Level()
    level.nbr_drones = 2

    from parsing.plateform import Hub
    hub1 = Hub("start", (0, 0))
    hub1.zone = "start"
    level.start_hub = hub1
    level.hub["start"] = hub1
    hub2 = Hub("end", (5, 5))
    hub2.zone = "end"
    level.end_hub = hub2
    level.hub["end"] = hub2
    main(level)
