import arcade

from src import settings
from src.entities.bullet import Bullet
from src.entities.player import Player


class BulletManager:
    def __init__(self):
        self.bullets = arcade.SpriteList()

    def shoot(self, player: Player):
        if len(self.bullets) >= settings.BULLET_LIMIT:
            return None
        bullet = Bullet(player.center_x, player.top, settings.BULLET_SPEED)
        self.bullets.append(bullet)
        return bullet

    def update(self):
        self.bullets.update()
        for bullet in self.bullets[:]:
            if bullet.bottom > settings.SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()