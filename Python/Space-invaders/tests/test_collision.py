from unittest.mock import Mock

from src.core.collision import bullet_hits_enemy


def test_bullet_hits_enemy_returns_true_when_sprite_collides():
    bullet = Mock()
    enemy = Mock()
    bullet.collides_with_sprite.return_value = True

    assert bullet_hits_enemy(bullet, enemy) is True


def test_bullet_hits_enemy_returns_false_when_sprite_does_not_collide():
    bullet = Mock()
    enemy = Mock()
    bullet.collides_with_sprite.return_value = False

    assert bullet_hits_enemy(bullet, enemy) is False