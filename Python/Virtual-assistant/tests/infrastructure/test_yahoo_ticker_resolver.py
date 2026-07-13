from infrastructure.yahoo_ticker_resolver import YahooTickerResolver


def test_resuelve_el_ticker_correctamente(mocker):
    resultado_falso = mocker.Mock()
    resultado_falso.quotes = [{'symbol': 'AMZN'}]
    mocker.patch('infrastructure.yahoo_ticker_resolver.yf.Search', return_value=resultado_falso)

    resolver = YahooTickerResolver()
    ticker = resolver.resolver('amazon')

    assert ticker == 'AMZN'


def test_devuelve_none_si_no_hay_resultado(mocker):
    resultado_falso = mocker.Mock()
    resultado_falso.quotes = []
    mocker.patch('infrastructure.yahoo_ticker_resolver.yf.Search', return_value=resultado_falso)

    resolver = YahooTickerResolver()
    ticker = resolver.resolver('empresa que no existe')

    assert ticker is None


def test_devuleve_none_si_la_api_falla(mocker):
    mocker.patch('infrastructure.yahoo_ticker_resolver.yf.Search', side_effect=Exception('timeout'))

    resolver = YahooTickerResolver()
    ticker = resolver.resolver('amazon')

    assert ticker is None