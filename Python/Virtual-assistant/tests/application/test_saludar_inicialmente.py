import datetime

from application.use_cases.saludar_inicialmente import SaludarInicialmente


def test_saluda_buenos_dias_en_la_manana(mocker):
    synthesizer_falso = mocker.Mock()
    mocker.patch(
        'application.use_cases.saludar_inicialmente.datetime',
        wraps = datetime,
    ).datetime.now.return_value = datetime.datetime(2026, 1, 1, 8, 0)

    use_case = SaludarInicialmente(synthesizer_falso)

    use_case.ejecutar()

    synthesizer_falso.hablar.assert_called_once()
    mensaje_dicho = synthesizer_falso.hablar.call_args[0][0]
    assert 'Buenos días' in mensaje_dicho


def test_obtener_momento_del_dia_manana():
    assert SaludarInicialmente._obtener_momento_del_dia(8) == 'Buenos días'

def test_obtener_momento_del_dia_tarde():
    assert SaludarInicialmente._obtener_momento_del_dia(15) == 'Buenas tardes'

def test_obtener_momento_del_dia_noche():
    assert SaludarInicialmente._obtener_momento_del_dia(22) == 'Buenas noches'