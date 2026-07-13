import speech_recognition as sr

from domain.ports.speech_recognizer import SpeechRecognizer


class GoogleSpeechRecognizer(SpeechRecognizer):
    
    def __init__(self, idioma: str = "es-co", pause_threshold: float = 0.8):
        self._idioma = idioma
        self._pause_threshold = pause_threshold

    def escuchar(self) -> str:
        reconocedor = sr.Recognizer()

        with sr.Microphone() as origen:
            reconocedor.pause_threshold = self._pause_threshold
            print("Ya puedes hablar.")
            audio = reconocedor.listen(origen)

        try:
            pedido = reconocedor.recognize_google(audio, language=self._idioma)
            print("Dijiste: " + pedido)
            return pedido
        except sr.UnknownValueError:
            print("No entendí")
            return "Sigo esperando"
        except sr.RequestError:
            print("No hay servicio")
            return "Sigo esperando"
        except Exception:
            print("Algo salió mal")
            return "Sigo esperando"