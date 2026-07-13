import arcade

from src import settings


class Bullet(arcade.Sprite):
    def __init__(self, center_x: float, center_y: float, speed: float):
        super().__init__(center_x=center_x, center_y=center_y)
        self.change_y = speed
        if settings.PROJECTILE_TEXTURE.exists():
            self.texture = arcade.load_texture(str(settings.PROJECTILE_TEXTURE))
            self.width = 16
            self.height = 32
        else:
            self.texture = arcade.make_soft_square_texture(8, arcade.color.WHITE, outer_alpha=255)
            self.width = 8
            self.height = 18