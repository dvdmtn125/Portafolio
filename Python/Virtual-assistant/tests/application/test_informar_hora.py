import datetime

from application.use_cases.informar_hora import InformarHora


def test_informa_la_hora_correcta(mocker):
    synthesizer_falso = mocker.Mock()

    mocker.patch(
        'application.use_cases.informar_hora.datetime'
    ).datetime.now.return_value = datetime.datetime(2026, 1, 1, 14, 30, 45)

    use_case = InformarHora(synthesizer_falso)
    use_case.ejecutar()

    synthesizer_falso.hablar.assert_called_once_with(
        'En este momento son las 14 horas con 30 minutos y 45 segundos'
    )