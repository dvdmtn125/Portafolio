import webbrowser

from domain.ports.web_launcher import WebLauncher


class WebbrowserWebLauncher(WebLauncher):

    def abrir(self, url: str) -> None:
        webbrowser.open(url)