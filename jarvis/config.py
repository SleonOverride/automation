from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(slots=True)
class JarvisConfig:
    wake_word: str = "jarvis"
    owner_name: str = "Boss"
    memory_file: Path = Path("jarvis_memory.json")
    reminders_file: Path = Path("jarvis_reminders.json")
    log_file: Path = Path("jarvis.log")
    weather_location: str = ""
    enable_voice: bool = False

    @classmethod
    def from_env(cls) -> "JarvisConfig":
        return cls(
            wake_word=os.getenv("JARVIS_WAKE_WORD", "jarvis"),
            owner_name=os.getenv("JARVIS_OWNER", "Boss"),
            memory_file=Path(os.getenv("JARVIS_MEMORY_FILE", "jarvis_memory.json")),
            reminders_file=Path(os.getenv("JARVIS_REMINDERS_FILE", "jarvis_reminders.json")),
            log_file=Path(os.getenv("JARVIS_LOG_FILE", "jarvis.log")),
            weather_location=os.getenv("JARVIS_WEATHER_LOCATION", ""),
            enable_voice=os.getenv("JARVIS_ENABLE_VOICE", "false").lower() == "true",
        )
