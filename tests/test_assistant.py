from pathlib import Path

from jarvis.assistant import JarvisAssistant
from jarvis.config import JarvisConfig
from jarvis.io import BaseIO


class DummyIO(BaseIO):
    def listen(self) -> str:
        return ""

    def speak(self, text: str) -> None:
        pass


def test_memory_and_recall(tmp_path: Path):
    cfg = JarvisConfig(
        memory_file=tmp_path / "memory.json",
        reminders_file=tmp_path / "reminders.json",
        log_file=tmp_path / "jarvis.log",
    )
    assistant = JarvisAssistant(cfg, DummyIO())
    remember = assistant.handle("remember mark 42 is ready")
    recall = assistant.handle("recall")
    assert "Saved" in remember
    assert "mark 42 is ready" in recall


def test_security_mode(tmp_path: Path):
    cfg = JarvisConfig(
        memory_file=tmp_path / "memory.json",
        reminders_file=tmp_path / "reminders.json",
        log_file=tmp_path / "jarvis.log",
    )
    assistant = JarvisAssistant(cfg, DummyIO())
    assert assistant.handle("arm security") == "Security protocol armed."
    assert "Security mode active" in assistant.handle("unknown command")
