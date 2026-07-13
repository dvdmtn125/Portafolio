from src.entities.bullet import Bullet
from src.entities.enemy import Enemy


def bullet_hits_enemy(bullet: Bullet, enemy: Enemy) -> bool:
    return bullet.collides_with_sprite(enemy)