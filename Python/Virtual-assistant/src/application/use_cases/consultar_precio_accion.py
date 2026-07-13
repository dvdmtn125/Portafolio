from domain.ports.speech_synthesizer import SpeechSynthesizer
from domain.ports.stock_price_provider import StockPriceProvider
from domain.ports.ticker_resolver import TicketResolver


class ConsultarPrecioAccion:

    def __init__(
            self,
            synthesizer: SpeechSynthesizer,
            stock_provider: StockPriceProvider,
            ticket_resolver: TicketResolver,
    ):
        self._synthesizer = synthesizer
        self._stock_provider = stock_provider
        self._ticket_resolver = ticket_resolver

    def ejecutar(self, nombre_empresa: str) -> None:
        nombre_empresa = nombre_empresa.strip().lower()
        simbolo = self._ticket_resolver.resolver(nombre_empresa)

        if simbolo is None:
            self._synthesizer.hablar('No pude encontrar la información solicitada')
            return
        
        try:
            precio = self._stock_provider.obtener_precio(simbolo)
            self._synthesizer.hablar(f'Esto fue lo que encontré, El precio de {nombre_empresa} es {precio}')
        except Exception:
            self._synthesizer.hablar('No pude encontrar la información solicitada')