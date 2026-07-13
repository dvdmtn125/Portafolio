from application.use_cases.buscar_en_wikipedia import BuscarEnWikipedia


def test_busca_y_dice_el_resumen(mocker):
    synthesizer_falso = mocker.Mock()
    Knowledge_source_falso = mocker.Mock()
    Knowledge_source_falso.buscar_resumen.return_value = 'Colombia es un país de Sudamérica'

    use_case = BuscarEnWikipedia(synthesizer_falso, Knowledge_source_falso)
    use_case.ejecutar('colombia')

    Knowledge_source_falso.buscar_resumen.assert_called_once_with('colombia')
    assert synthesizer_falso.hablar.call_count == 3