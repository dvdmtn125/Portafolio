import pyjokes

from domain.ports.joke_provider import JokeProvider


class PyjokesJokeProvider(JokeProvider):

    def __init__(self, idioma: str = "es"):
        self._idioma = idioma

    def obtener_chiste(self) -> str:
        return pyjokes.get_joke(self._idioma)