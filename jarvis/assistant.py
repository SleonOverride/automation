from __future__ import annotations

from dataclasses import dataclass
import logging

from jarvis.config import JarvisConfig
from jarvis.intents import parse_intent
from jarvis.io import BaseIO
from jarvis.skills.core import CoreSkills, SkillContext


@dataclass
class SecurityState:
    armed: bool = False


class JarvisAssistant:
    def __init__(self, cfg: JarvisConfig, io_backend: BaseIO):
        self.cfg = cfg
        self.io = io_backend
        self.security = SecurityState()
        logging.basicConfig(filename=cfg.log_file, level=logging.INFO)
        self.skills = CoreSkills(
            SkillContext(
                owner_name=cfg.owner_name,
                memory_file=cfg.memory_file,
                reminders_file=cfg.reminders_file,
                weather_location=cfg.weather_location,
            )
        )

    def startup_message(self) -> str:
        return (
            f"Online and ready, {self.cfg.owner_name}. "
            "Type help to view available capabilities."
        )

    def handle(self, text: str) -> str:
        intent = parse_intent(text)
        logging.info("intent=%s text=%s", intent.name, text)

        match intent.name:
            case "empty":
                return "I didn't catch that."
            case "help":
                return self._help()
            case "shutdown":
                return "Powering down."
            case "time":
                return self.skills.now()
            case "date":
                return self.skills.date()
            case "weather":
                return self.skills.weather()
            case "system_status":
                return self.skills.system_status()
            case "remember":
                return self.skills.remember(text)
            case "recall":
                return self.skills.recall()
            case "reminder":
                return self.skills.set_reminder(text)
            case "list_reminders":
                return self.skills.list_reminders()
            case "search_web":
                return self.skills.search_web(text)
            case "open_app":
                return self.skills.open_app(text)
            case "run_command":
                return self.skills.run_command(text)
            case "arm_security":
                self.security.armed = True
                return "Security protocol armed."
            case "disarm_security":
                self.security.armed = False
                return "Security protocol disarmed."
            case "smart_home":
                return self.skills.smart_home(text)
            case _:
                if self.security.armed:
                    return "Security mode active. Unknown request recorded."
                return (
                    "I can help with reminders, memory, web search, system checks, "
                    "smart-home simulation, and safe terminal commands."
                )

    def run(self) -> None:
        self.io.speak(self.startup_message())
        while True:
            heard = self.io.listen()
            response = self.handle(heard)
            self.io.speak(response)
            if "powering down" in response.lower():
                break

    def _help(self) -> str:
        return (
            "Capabilities: time/date, weather, system status, remember/recall notes, "
            "set/list reminders, web search, open shortcuts, run safe terminal command, "
            "arm/disarm security, and smart-home simulation."
        )
