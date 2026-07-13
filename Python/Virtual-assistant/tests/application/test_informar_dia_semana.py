import datetime

from application.use_cases.informar_dia_semana import InformarDiaSemana


def test_informa_el_dia_correcto(mocker):
    synthesizer_falso = mocker.Mock()

    mocker.patch(
        'application.use_cases.informar_dia_semana.datetime'
    ).date.today.return_value = datetime.date(2026, 1, 1)

    use_case = InformarDiaSemana(synthesizer_falso)
    use_case.ejecutar()

    synthesizer_falso.hablar.assert_called_once_with('Hoy es Jueves')