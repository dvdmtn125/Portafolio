import pytest

from controllers.asistente_controller import AsistenteController


@pytest.fixture
def controller(mocker):
    return AsistenteController(
        recognizer=mocker.Mock(),
        synthesizer=mocker.Mock(),
        saludar_inicialmente=mocker.Mock(),
        informar_dia_semana=mocker.Mock(),
        informar_hora=mocker.Mock(),
        buscar_en_wikipedia=mocker.Mock(),
        buscar_en_internet=mocker.Mock(),
        reproducir_video=mocker.Mock(),
        contar_chiste=mocker.Mock(),
        consultar_precio_accion=mocker.Mock(),
        abrir_pagina_web=mocker.Mock(),
        despedirse=mocker.Mock(),
    )


def test_abre_youtube(controller):
    continuar = controller._procesar_comando('abre youtube')

    controller._abrir_pagina_web.ejecutar.assert_called_once_with(
        url='https://www.youtube.com/',
        mensaje_previo='Con gusto, Estoy abriendo youtube',
    )
    assert continuar is True


def test_abre_el_navegador(controller):
    continuar = controller._procesar_comando('abre el navegador')

    controller._abrir_pagina_web.ejecutar.assert_called_once_with(
        url='https://www.google.com/',
        mensaje_previo='Claro, estoy en eso',
    )
    assert continuar is True


def test_pregunta_que_dia_es_hoy(controller):
    continuar = controller._procesar_comando('qué día es hoy')

    controller._informar_dia_semana.ejecutar.assert_called_once_with()
    assert continuar is True


def test_pregunta_que_hora_es(controller):
    continuar = controller._procesar_comando('qué hora es')

    controller._informar_hora.ejecutar.assert_called_once_with()
    assert continuar is True


def test_busca_en_wikipedia_extrae_la_consulta(controller):
    continuar = controller._procesar_comando('busca en wikipedia colombia')

    controller._buscar_en_wikipedia.ejecutar.assert_called_once_with('colombia')
    assert continuar is True


def test_busca_en_internet_extrae_la_consulta(controller):
    continuar = controller._procesar_comando('busca en internet recetas para pasta')

    controller._buscar_en_internet.ejecutar.assert_called_once_with('recetas para pasta')
    assert continuar is True


def test_reproduce_video(controller):
    continuar = controller._procesar_comando('reproduce despacito')

    controller._reproducir_video.ejecutar.assert_called_once_with('reproduce despacito')
    assert continuar is True


def test_pide_un_chiste(controller):
    continuar = controller._procesar_comando('cuéntame un chiste')

    controller._contar_chiste.ejecutar.assert_called_once_with()
    assert continuar is True


def test_consulta_precio_de_acciones(controller):
    continuar = controller._procesar_comando('precio de las acciones de amazon')

    controller._consultar_precio_accion.ejecutar.assert_called_once_with('amazon')
    assert continuar is True


def test_se_despide_y_detiene_el_loop(controller):
    continuar = controller._procesar_comando('adiós')

    controller._despedirse.ejecutar.assert_called_once_with()
    assert continuar is False


def test_comando_no_reconocido_no_ejecuta_nada(controller):
    continuar = controller._procesar_comando('esto no significa nada')

    controller._saludar_inicialmente.ejecutar.assert_not_called()
    controller._informar_dia_semana.ejecutar.assert_not_called()
    controller._informar_hora.ejecutar.assert_not_called()
    controller._buscar_en_wikipedia.ejecutar.assert_not_called()
    controller._buscar_en_internet.ejecutar.assert_not_called()
    controller._reproducir_video.ejecutar.assert_not_called()
    controller._contar_chiste.ejecutar.assert_not_called()
    controller._consultar_precio_accion.ejecutar.assert_not_called()
    controller._abrir_pagina_web.ejecutar.assert_not_called()
    controller._despedirse.ejecutar.assert_not_called()
    assert continuar is True