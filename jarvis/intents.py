from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Intent:
    name: str
    payload: str = ""


def parse_intent(user_text: str) -> Intent:
    text = user_text.strip().lower()
    if not text:
        return Intent("empty")

    mappings = {
        "shutdown": ["shutdown", "goodbye", "exit", "quit"],
        "time": ["time", "what time"],
        "date": ["date", "what day"],
        "weather": ["weather", "temperature", "forecast"],
        "system_status": ["system status", "cpu", "memory", "battery"],
        "remember": ["remember", "note this"],
        "recall": ["what do you remember", "recall", "memory"],
        "reminder": ["remind me", "set reminder"],
        "list_reminders": ["list reminders", "my reminders"],
        "search_web": ["search", "look up", "google"],
        "open_app": ["open ", "launch "],
        "run_command": ["run command", "terminal"],
        "arm_security": ["arm security", "activate security"],
        "disarm_security": ["disarm security", "security off"],
        "smart_home": ["lights", "smart home", "temperature set"],
        "help": ["help", "abilities", "what can you do"],
    }

    for name, triggers in mappings.items():
        if any(trigger in text for trigger in triggers):
            return Intent(name, user_text)

    return Intent("general", user_text)
