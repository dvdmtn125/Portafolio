import arcade

from src import settings


class Hud:
    def draw(self, score: int):
        arcade.draw_text(
            f"Puntaje: {score}",
            20,
            settings.SCREEN_HEIGHT - 36,
            arcade.color.WHITE,
            settings.HUD_TEXT_SIZE,
            font_name=str(settings.DEFAULT_FONT) if settings.DEFAULT_FONT.exists() else None,
        )