import logging
import time
from typing import List

import requests
from bs4 import BeautifulSoup

from application.interfaces import QuoteScraperPort
from domain.entities import Quote

logger = logging.getLogger(__name__)


class BeautifulSoupQuoteScraper(QuoteScraperPort):

    BASE_URL = "https://quotes.toscrape.com"
    HEADERS = {
        "user-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
    }

    def __init__(self, delay_seconds: float = 1.0, timeout: int = 10):
        self._delay = delay_seconds
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(self.HEADERS)

    def fetch_quotes(self, max_pages: int = 5) -> List[Quote]:
        quotes: List[Quote] = []
        page = 1

        while page <= max_pages:
            url = f"{self.BASE_URL}/page/{page}/"
            html = self._get_html(url)

            if html is None:
                break

            page_quotes = self._parse_quotes(html)
            if not page_quotes:
                logger.info("No hay más citas. Fin en la pagina %s.", page)
                break
            quotes.extend(page_quotes)
            logger.debug("Página %s -> %s citas extraídas.",
                          page, len(page_quotes))
            
            page += 1
            time.sleep(self._delay)

        return quotes
    
    def _get_html(self, url: str) -> str | None:
        try:
            response = self._session.get(url, timeout=self._timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            logger.error("Error al solicitar %s: %s", url, exc)
            return None
        
    @staticmethod
    def _parse_quotes(html: str) -> List[Quote]:
        soup = BeautifulSoup(html, "html.parser")
        blocks = soup.select("div.quote")

        result: List[Quote] = []
        for block in blocks:
            text_el = block.select_one("span.text")
            author_el = block.select_one("small.author")
            tag_els = block.select("div.tags a.tag")

            if not text_el or not author_el:
                continue

            result.append(
                Quote(
                    text=text_el.get_text(strip=True),
                    author=author_el.get_text(strip=True),
                    tags=[t.get_text(strip=True) for t in tag_els],
                )
            )
        return result