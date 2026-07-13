from application.use_cases.contar_chiste import ContarChiste


def test_cuenta_el_chiste_obteniendo(mocker):
    synthesizer_falso = mocker.Mock()
    joke_provider_falso = mocker.Mock()
    joke_provider_falso.obtener_chiste.return_value = '¿Por qué los pájaros vuelan hacia el sur? Porque es muy largo para caminar'

    use_case = ContarChiste(synthesizer_falso, joke_provider_falso)
    use_case.ejecutar()

    synthesizer_falso.hablar.assert_called_once_with(
        '¿Por qué los pájaros vuelan hacia el sur? Porque es muy largo para caminar'
    )