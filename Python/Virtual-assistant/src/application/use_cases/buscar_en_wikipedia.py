from domain.ports.speech_synthesizer import SpeechSynthesizer
from domain.ports.knowledge_source import KnowledgeSource


class BuscarEnWikipedia:

    def __init__(self, synthesizer: SpeechSynthesizer, knowledge_source: KnowledgeSource):
        self._synthesizer = synthesizer
        self._knowledge_source = knowledge_source

    def ejecutar(self, consulta: str) -> None:
        self._synthesizer.hablar('Buscando eso en Wikipedia')
        resumen = self._knowledge_source.buscar_resumen(consulta)
        self._synthesizer.hablar('Wikipedia dice lo siguiente: ')
        self._synthesizer.hablar(resumen)
