import datetime

from application.use_cases.despedirse import Despedirse


def test_se_despide_con_feliz_dia_en_la_manana(mocker):
    synthesizer_falso = mocker.Mock()
    mocker.patch(
        'application.use_cases.despedirse.datetime'
    ).datetime.now.return_value = datetime.datetime(2026, 1, 1, 9, 0)

    use_case = Despedirse(synthesizer_falso)
    use_case.ejecutar()

    synthesizer_falso.hablar.assert_called_once_with('Feliz día')


def test_se_despide_con_feliz_noche_de_madrugada(mocker):
    synthesizer_falso = mocker.Mock()
    mocker.patch(
        'application.use_cases.despedirse.datetime'
    ).datetime.now.return_value = datetime.datetime(2026, 1, 1, 3, 0)

    use_case = Despedirse(synthesizer_falso)
    use_case.ejecutar()

    synthesizer_falso.hablar.assert_called_once_with('Feliz noche')