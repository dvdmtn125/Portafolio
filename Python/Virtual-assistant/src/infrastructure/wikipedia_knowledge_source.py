import wikipedia

from domain.ports.knowledge_source import KnowledgeSource


class WikipediaKnowledgeSource(KnowledgeSource):

    def __init__(self, idioma: str = "es"):
        wikipedia.set_lang(idioma)

    def buscar_resumen(self, consulta: str) -> str:
        return wikipedia.summary(consulta, sentences=1)