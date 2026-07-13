from pathlib import Path

import arcade

from src import settings


class Player(arcade.Sprite):
    def __init__(self, texture_path: Path):
        super().__init__(center_x=settings.PLAYER_START_X, center_y=settings.PLAYER_START_Y)
        self.change_x = 0
        self._set_texture(texture_path)

    def _set_texture(self, texture_path: Path):
        if texture_path.exists():
            self.texture = arcade.load_texture(str(texture_path))
        else:
            self.texture = arcade.make_soft_square_texture(48, arcade.color.SKY_BLUE, outer_alpha=255)
        self.width = 48
        self.height = 48

    def update(self):
        self.center_x += self.change_x
        self.center_x = max(settings.PLAYER_BOUNDARY_LEFT, self.center_x)
        self.center_x = min(settings.PLAYER_BOUNDARY_RIGHT, self.center_x)