from pathlib import Path

import arcade


class Enemy(arcade.Sprite):
    def __init__(self, texture_path: Path, center_x: float, center_y: float, speed: float):
        super().__init__(center_x=center_x, center_y=center_y)
        self.change_x = speed
        self._set_texture(texture_path)

    def _set_texture(self, texture_path: Path):
        if texture_path.exists():
            self.texture = arcade.load_texture(str(texture_path))
        else:
            self.texture = arcade.make_soft_square_texture(40, arcade.color.RADICAL_RED, outer_alpha=255)
        self.width = 40
        self.height = 40