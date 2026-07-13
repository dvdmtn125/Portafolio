from application.use_cases.buscar_en_internet import BuscarEnInternet


def test_busca_en_internet(mocker):
    synthesizer_falso = mocker.Mock()
    web_searcher_falso = mocker.Mock()

    use_case = BuscarEnInternet(synthesizer_falso, web_searcher_falso)
    use_case.ejecutar('recetas de pasta')

    web_searcher_falso.buscar.assert_called_once_with('recetas de pasta')
    assert synthesizer_falso.hablar.call_count == 2