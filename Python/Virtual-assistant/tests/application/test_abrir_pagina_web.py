from application.use_cases.abrir_pagina_web import AbrirPaginaWeb


def test_abre_la_url_indicada(mocker):
    synthesizer_falso = mocker.Mock()
    web_launcher_falso = mocker.Mock()

    use_case = AbrirPaginaWeb(synthesizer_falso, web_launcher_falso)
    use_case.ejecutar(url='https://www.youtube.com/', mensaje_previo='Abriendo youtube')

    synthesizer_falso.hablar.assert_called_once_with('Abriendo youtube')
    web_launcher_falso.abrir.assert_called_once_with('https://www.youtube.com/')