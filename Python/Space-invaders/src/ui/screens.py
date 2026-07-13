import arcade

from src import settings


class StartScreenView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            settings.SCREEN_TITLE,
            settings.SCREEN_WIDTH / 2,
            settings.SCREEN_HEIGHT / 2 + 40,
            arcade.color.WHITE,
            settings.TITLE_TEXT_SIZE,
            anchor_x="center",
            font_name=str(settings.DEFAULT_FONT) if settings.DEFAULT_FONT.exists() else None,
        )
        arcade.draw_text(
            "Presiona ENTER para comenzar",
            settings.SCREEN_WIDTH / 2,
            settings.SCREEN_HEIGHT / 2 - 10,
            arcade.color.LIGHT_GRAY,
            settings.SUBTITLE_TEXT_SIZE,
            anchor_x="center",
            font_name=str(settings.DEFAULT_FONT) if settings.DEFAULT_FONT.exists() else None,
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            self.window.start_game()


class GameOverView(arcade.View):
    def __init__(self, score: int):
        super().__init__()
        self.score = score

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "JUEGO TERMINADO",
            settings.SCREEN_WIDTH / 2,
            settings.SCREEN_HEIGHT / 2 + 30,
            arcade.color.WHITE,
            settings.TITLE_TEXT_SIZE,
            anchor_x="center",
            font_name=str(settings.DEFAULT_FONT) if settings.DEFAULT_FONT.exists() else None,
        )
        arcade.draw_text(
            f"Puntaje final: {self.score}",
            settings.SCREEN_WIDTH / 2,
            settings.SCREEN_HEIGHT / 2 - 20,
            arcade.color.WHITE,
            settings.HUD_TEXT_SIZE,
            anchor_x="center",
            font_name=str(settings.DEFAULT_FONT) if settings.DEFAULT_FONT.exists() else None,
        )
        arcade.draw_text(
            "Presiona R para reiniciar",
            settings.SCREEN_WIDTH / 2,
            settings.SCREEN_HEIGHT / 2 - 60,
            arcade.color.LIGHT_GRAY,
            settings.SUBTITLE_TEXT_SIZE,
            anchor_x="center",
            font_name=str(settings.DEFAULT_FONT) if settings.DEFAULT_FONT.exists() else None,
        )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            self.window.start_game()