from application.use_cases.reproducir_video import ReproducirVideo


def test_reproduce_el_video_solicitado(mocker):
    synthesizer_falso = mocker.Mock()
    video_player_falso = mocker.Mock()

    use_case = ReproducirVideo(synthesizer_falso, video_player_falso)
    use_case.ejecutar('reproduce despacito')

    video_player_falso.reproducir.assert_called_once_with('reproduce despacito')
    synthesizer_falso.hablar.assert_called_once_with('Reproduciendo')