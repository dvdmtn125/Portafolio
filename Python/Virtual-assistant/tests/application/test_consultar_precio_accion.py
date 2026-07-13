from application.use_cases.consultar_precio_accion import ConsultarPrecioAccion


def test_consulta_precio_exitosamente(mocker):
    synthesizer_falso = mocker.Mock()
    stock_provider_falso = mocker.Mock()
    ticket_provider_falso = mocker.Mock()

    ticket_provider_falso.resolver.return_value = 'AMZN'
    stock_provider_falso.obtener_precio.return_value = 185.42

    use_case = ConsultarPrecioAccion(synthesizer_falso, stock_provider_falso, ticket_provider_falso)
    use_case.ejecutar('amazon')

    ticket_provider_falso.resolver.assert_called_once_with('amazon')
    stock_provider_falso.obtener_precio.assert_called_once_with('AMZN')
    synthesizer_falso.hablar.assert_called_once_with(
        'Esto fue lo que encontré, El precio de amazon es 185.42'
    )

def test_no_encuentra_el_ticker_de_la_empresa(mocker):
    synthesizer_falso = mocker.Mock()
    stock_provider_falso = mocker.Mock()
    ticket_provider_falso = mocker.Mock()

    ticket_provider_falso.resolver.return_value = None

    use_case = ConsultarPrecioAccion(synthesizer_falso, stock_provider_falso, ticket_provider_falso)
    use_case.ejecutar('empresa inventada')

    stock_provider_falso.obtener_precio.assert_not_called()
    synthesizer_falso.hablar.assert_called_once_with('No pude encontrar la información solicitada')


def test_falla_al_consultar_el_precio(mocker):
    synthesizer_falso = mocker.Mock()
    stock_provider_falso = mocker.Mock()
    ticket_provider_falso = mocker.Mock()

    ticket_provider_falso.resolver.return_value = 'AAPL'
    stock_provider_falso.obtener_precio.side_effect = Exception('API caída')

    use_case = ConsultarPrecioAccion(synthesizer_falso, stock_provider_falso, ticket_provider_falso)
    use_case.ejecutar('apple')

    synthesizer_falso.hablar.assert_called_once_with('No pude encontrar la información solicitada')