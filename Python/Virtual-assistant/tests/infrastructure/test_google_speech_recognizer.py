import speech_recognition as sr

from infrastructure.google_speech_recognizer import GoogleSpeechRecognizer


def test_reconoce_el_audio_correctamente(mocker):
    reconocedor_falso = mocker.Mock()
    reconocedor_falso.recognize_google.return_value = 'abre youtube'
    mocker.patch('infrastructure.google_speech_recognizer.sr.Recognizer', return_value=reconocedor_falso)
    mocker.patch('infrastructure.google_speech_recognizer.sr.Microphone')

    recognizer = GoogleSpeechRecognizer()
    resultado = recognizer.escuchar()

    assert resultado == 'abre youtube'


def test_no_entiende_el_audio(mocker):
    reconocedor_falso = mocker.Mock()
    reconocedor_falso.recognize_google.side_effect = sr.UnknownValueError()
    mocker.patch('infrastructure.google_speech_recognizer.sr.Recognizer', return_value=reconocedor_falso)
    mocker.patch('infrastructure.google_speech_recognizer.sr.Microphone')

    recognizer = GoogleSpeechRecognizer()
    resultado = recognizer.escuchar()

    assert resultado == 'Sigo esperando'


def test_no_hay_servicio_disponible(mocker):
    reconocedor_falso = mocker.Mock()
    reconocedor_falso.recognize_google.side_effect = sr.RequestError()
    mocker.patch('infrastructure.google_speech_recognizer.sr.Recognizer', return_value=reconocedor_falso)
    mocker.patch('infrastructure.google_speech_recognizer.sr.Microphone')

    recognizer = GoogleSpeechRecognizer()
    resultado = recognizer.escuchar()

    assert resultado == 'Sigo esperando'

def test_error_inesperado(mocker):
    reconocedor_falso = mocker.Mock()
    reconocedor_falso.recognize_google.side_effect = ValueError('algo raro pasó')
    mocker.patch('infrastructure.google_speech_recognizer.sr.Recognizer', return_value=reconocedor_falso)
    mocker.patch('infrastructure.google_speech_recognizer.sr.Microphone')

    recognizer = GoogleSpeechRecognizer()
    resultado = recognizer.escuchar()

    assert resultado == 'Sigo esperando'