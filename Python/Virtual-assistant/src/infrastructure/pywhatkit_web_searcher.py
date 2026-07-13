import pywhatkit

from domain.ports.web_searcher import WebSearcher


class PywhatkitWebSearcher(WebSearcher):

    def buscar(self, consulta: str) -> None:
        pywhatkit.search(consulta)