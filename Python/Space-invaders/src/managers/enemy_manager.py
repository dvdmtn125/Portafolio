import random

import arcade

from src import settings
from src.entities.enemy import Enemy


class EnemyManager:
    def __init__(self):
        self.enemies = arcade.SpriteList()

    def spawn_wave(self):
        self.enemies.clear()
        for _ in range(settings.ENEMY_COUNT):
            enemy = Enemy(
                texture_path=settings.ENEMY_TEXTURE,
                center_x=random.randint(40, settings.SCREEN_WIDTH - 40),
                center_y=random.randint(settings.ENEMY_MIN_Y, settings.ENEMY_MAX_Y),
                speed=settings.ENEMY_SPEED,
            )
            self.enemies.append(enemy)

    def update(self):
        for enemy in self.enemies:
            enemy.center_x += enemy.change_x
            if enemy.left <= 0 or enemy.right >= settings.SCREEN_WIDTH:
                enemy.change_x *= -1
                enemy.center_y -= settings.ENEMY_DROP_DISTANCE

    def reset_enemy(self, enemy: Enemy):
        enemy.center_x = random.randint(40, settings.SCREEN_WIDTH - 40)
        enemy.center_y = random.randint(settings.ENEMY_MIN_Y, settings.ENEMY_MAX_Y)