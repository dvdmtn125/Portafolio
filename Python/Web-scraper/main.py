import argparse
import logging
import sys

from application.use_cases import ScrapeQuotesUseCase
from infrastructure.scraper import BeautifulSoupQuoteScraper
from infrastructure.repository import CsvQuoteRepository, JsonQuoteRepository

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scraper de citas (quotes.toscrape.com)")
    parser.add_argument(
        "--pages", type=int, default=5, help="Número máximo de páginas a recorrer."
    )
    parser.add_argument(
    "--format", choices=["csv", "json"], default="csv", help="Formato de salida."
    )
    parser.add_argument(
        "--output", type=str, default=None, help="Ruta del archivo de salida (JSON o CSV)."
    )
    parser.add_argument(
        "--delay", type=float, default=1.0, help="Retraso entre solicitudes (en segundos)."
    )
    return parser.parse_args()


def main():
    configure_logging()
    args = parse_args()

    scraper = BeautifulSoupQuoteScraper(delay_seconds=args.delay)

    if args.format == "json":
        output_path = args.output or "output/quotes.json"
        repository = JsonQuoteRepository(file_path=output_path)
    else:
        output_path = args.output or "output/quotes.csv"
        repository = CsvQuoteRepository(file_path=output_path)

    use_case = ScrapeQuotesUseCase(scraper=scraper, repository=repository)
    quotes = use_case.execute(max_pages=args.pages)

    if not quotes:
        return 1
    
    print(f"\nListo: {len(quotes)} citas guardadas en '{output_path}'\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
