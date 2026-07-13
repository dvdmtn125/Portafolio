from typing import Optional

import yfinance as yf

from domain.ports.ticker_resolver import TicketResolver


class YahooTickerResolver(TicketResolver):

    def resolver(self, nombre_empresa: str) -> Optional[str]:
        try:
            resultado = yf.Search(nombre_empresa, max_results=1)
            cotizaciones = resultado.quotes

            if not cotizaciones:
                return None
            
            return cotizaciones[0]['symbol']
        except Exception:
            return None