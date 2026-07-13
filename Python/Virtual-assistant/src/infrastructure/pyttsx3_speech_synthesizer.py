import pyttsx3

from domain.ports.speech_synthesizer import SpeechSynthesizer


class Pyttsx3SpeechSynthesizer(SpeechSynthesizer):
    
    _VOZ_ESPANOL = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'

    def hablar(self, mensaje: str) -> None:
        motor = pyttsx3.init()
        motor.setProperty('voice', self._VOZ_ESPANOL)
        motor.say(mensaje)
        motor.runAndWait()