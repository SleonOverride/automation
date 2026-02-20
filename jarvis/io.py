from __future__ import annotations

from dataclasses import dataclass


class BaseIO:
    def listen(self) -> str:
        raise NotImplementedError

    def speak(self, text: str) -> None:
        raise NotImplementedError


@dataclass
class TextIO(BaseIO):
    prompt: str = "You> "

    def listen(self) -> str:
        return input(self.prompt).strip()

    def speak(self, text: str) -> None:
        print(f"Jarvis> {text}")


class VoiceIO(BaseIO):
    def __init__(self) -> None:
        try:
            import pyttsx3
            import speech_recognition as sr
        except Exception as exc:  # pragma: no cover - optional dependency runtime
            raise RuntimeError(
                "Voice mode requires SpeechRecognition and pyttsx3 dependencies"
            ) from exc

        self._sr = sr
        self._recognizer = sr.Recognizer()
        self._tts = pyttsx3.init()

    def listen(self) -> str:
        with self._sr.Microphone() as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = self._recognizer.listen(source)
        try:
            return self._recognizer.recognize_google(audio).strip()
        except self._sr.UnknownValueError:
            return ""

    def speak(self, text: str) -> None:
        self._tts.say(text)
        self._tts.runAndWait()
