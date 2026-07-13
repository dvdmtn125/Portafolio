import logging
from typing import List

from domain.entities import Quote
from application.interfaces import QuoteScraperPort, QuoteRepositoryPort

logger = logging.getLogger(__name__)


class ScrapeQuotesUseCase:
    def __init__(self, scraper: QuoteScraperPort, repository: QuoteRepositoryPort):
        self._scraper = scraper
        self._repository = repository

    def execute(self, max_pages: int = 5) -> List[Quote]:
        logger.info("Iniciando extracción de citas (máx. %s páginas)...", 
                    max_pages)
        quotes = self._scraper.fetch_quotes(max_pages=max_pages)
        logger.info("Se extrajeron %s citas.", len(quotes))

        if not quotes:
            logger.warning("No se obtuvieron citas. Revisa la conexión a Internet o la estructura del sitio web.")
            return []
        
        self._repository.save(quotes)
        logger.info("Citas guardadas correctamente.")
        return quotes