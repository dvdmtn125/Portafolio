import yfinance as yf

from domain.ports.stock_price_provider import StockPriceProvider


class YfinanceStockPriceProvider(StockPriceProvider):

    def obtener_precio(self, simbolo: str) -> float:
        ticker = yf.Ticker(simbolo)
        return ticker.info['regularMarketPrice']