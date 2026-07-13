from pathlib import Path

import arcade

from src import settings
from src.core.collision import bullet_hits_enemy
from src.core.scoring import increase_score
from src.entities.player import Player
from src.managers.audio_manager import AudioManager
from src.managers.bullet_manager import BulletManager
from src.managers.enemy_manager import EnemyManager
from src.ui.hud import Hud
from src.ui.screens import GameOverView, StartScreenView


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.player = Player(settings.PLAYER_TEXTURE)
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        self.audio_manager = AudioManager()
        self.hud = Hud()
        self.score = 0

    def setup(self):
        self.background = self._load_background(settings.BACKGROUND_IMAGE)
        self.player = Player(settings.PLAYER_TEXTURE)
        self.enemy_manager = EnemyManager()
        self.enemy_manager.spawn_wave()
        self.bullet_manager = BulletManager()
        self.audio_manager = AudioManager()
        self.audio_manager.load(
            settings.BACKGROUND_MUSIC,
            settings.SHOOT_SOUND,
            settings.HIT_SOUND,
        )
        self.audio_manager.play_background()
        self.hud = Hud()
        self.score = 0

    def _load_background(self, path: Path):
        if path.exists():
            return arcade.load_texture(str(path))
        return None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rect(
                self.background,
                arcade.LRBT(
                    left=0,
                    right=settings.SCREEN_WIDTH,
                    bottom=0,
                    top=settings.SCREEN_HEIGHT,
                ),
            )
        self.enemy_manager.enemies.draw()
        self.bullet_manager.bullets.draw()
        arcade.draw_sprite(self.player)
        self.hud.draw(self.score)

    def on_update(self, delta_time: float):
        self.player.update()
        self.enemy_manager.update()
        self.bullet_manager.update()
        self._handle_collisions()
        self._check_game_over()

    def _handle_collisions(self):
        for bullet in self.bullet_manager.bullets[:]:
            for enemy in self.enemy_manager.enemies:
                if bullet_hits_enemy(bullet, enemy):
                    bullet.remove_from_sprite_lists()
                    self.enemy_manager.reset_enemy(enemy)
                    self.audio_manager.play_hit()
                    self.score = increase_score(self.score)
                    break

    def _check_game_over(self):
        for enemy in self.enemy_manager.enemies:
            if enemy.bottom <= settings.GAME_OVER_LINE:
                self.window.show_view(GameOverView(self.score))
                break

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.player.change_x = -settings.PLAYER_SPEED
        elif symbol == arcade.key.RIGHT:
            self.player.change_x = settings.PLAYER_SPEED
        elif symbol == arcade.key.SPACE:
            bullet = self.bullet_manager.shoot(self.player)
            if bullet is not None:
                self.audio_manager.play_shoot()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0


class SpaceInvadersGame(arcade.Window):
    def __init__(self):
        super().__init__(
            width=settings.SCREEN_WIDTH,
            height=settings.SCREEN_HEIGHT,
            title=settings.SCREEN_TITLE,
            update_rate=1 / 120,
        )

    def setup(self):
        self.show_view(StartScreenView())

    def start_game(self):
        game_view = GameView()
        game_view.setup()
        self.show_view(game_view)
