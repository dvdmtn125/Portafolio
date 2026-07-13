import csv
import json
import logging
from pathlib import Path
from typing import List

from application.interfaces import QuoteRepositoryPort
from domain.entities import Quote

logger = logging.getLogger(__name__)


class CsvQuoteRepository(QuoteRepositoryPort):
    def __init__(self, file_path: str):
        self._file_path = Path(file_path)

    def save(self, quotes:  List[Quote]) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)

        with self._file_path.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["text", "author", "tags"])
            writer.writeheader()
            for quote in quotes:
                row = quote.to_dict()
                row["tags"] = ", ".join(row["tags"])  # Convert list of tags to a comma-separated string
                writer.writerow(row)

        logger.info(f"CSV guardado en: %s", self._file_path)
    

class JsonQuoteRepository(QuoteRepositoryPort):
    def __init__(self, file_path: str):
        self._file_path = Path(file_path)

    def save(self, file_path: str = "output/quotes.json"):
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = [quote.to_dict() for quote in self.quotes]
        with self._file_path.open("w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
            
        logger.info(f"JSON guardado en: %s", self._file_path)