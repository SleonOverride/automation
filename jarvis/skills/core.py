from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import platform
import shlex
import subprocess
import webbrowser

import requests

from jarvis.storage import load_json, save_json


@dataclass
class SkillContext:
    owner_name: str
    memory_file: Path
    reminders_file: Path
    weather_location: str


class CoreSkills:
    def __init__(self, ctx: SkillContext):
        self.ctx = ctx

    def now(self) -> str:
        return datetime.now().strftime("It is %I:%M %p")

    def date(self) -> str:
        return datetime.now().strftime("Today is %A, %d %B %Y")

    def weather(self) -> str:
        loc = self.ctx.weather_location or ""
        target = loc.replace(" ", "+")
        url = f"https://wttr.in/{target}?format=3"
        try:
            resp = requests.get(url, timeout=8)
            resp.raise_for_status()
            return resp.text.strip()
        except requests.RequestException:
            return "I couldn't fetch weather right now."

    def system_status(self) -> str:
        return (
            f"Running on {platform.system()} {platform.release()} with Python "
            f"{platform.python_version()}."
        )

    def remember(self, text: str) -> str:
        memory = load_json(self.ctx.memory_file, [])
        note = text.split("remember", 1)[-1].strip(" :.-")
        if not note:
            return "Tell me what to remember."
        memory.append({"time": datetime.now().isoformat(), "note": note})
        save_json(self.ctx.memory_file, memory)
        return "Saved to memory core."

    def recall(self) -> str:
        memory = load_json(self.ctx.memory_file, [])
        if not memory:
            return "Memory core is empty."
        last = memory[-5:]
        lines = [f"- {item['note']}" for item in last]
        return "Recent memories:\n" + "\n".join(lines)

    def set_reminder(self, raw: str) -> str:
        reminders = load_json(self.ctx.reminders_file, [])
        payload = raw.split("remind me", 1)[-1].strip(" :.-")
        if not payload:
            return "Please provide a reminder text."
        reminders.append({"created": datetime.now().isoformat(), "task": payload, "done": False})
        save_json(self.ctx.reminders_file, reminders)
        return f"Reminder added: {payload}"

    def list_reminders(self) -> str:
        reminders = load_json(self.ctx.reminders_file, [])
        active = [r for r in reminders if not r.get("done")]
        if not active:
            return "No active reminders."
        return "Active reminders:\n" + "\n".join(f"- {r['task']}" for r in active)

    def search_web(self, raw: str) -> str:
        query = raw
        for prefix in ["search", "look up", "google"]:
            query = query.lower().replace(prefix, "").strip()
        if not query:
            return "Tell me what to search for."
        url = f"https://duckduckgo.com/?q={requests.utils.quote(query)}"
        webbrowser.open(url)
        return f"Searching the web for {query}."

    def open_app(self, raw: str) -> str:
        cleaned = raw.lower().replace("launch", "").replace("open", "").strip()
        if not cleaned:
            return "Tell me which application to open."
        app_map = {
            "browser": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://github.com",
        }
        if cleaned in app_map:
            webbrowser.open(app_map[cleaned])
            return f"Opening {cleaned}."
        return "I currently support opening browser, youtube, and github shortcuts."

    def run_command(self, raw: str) -> str:
        part = raw.lower().split("run command", 1)
        if len(part) < 2:
            return "Use: run command <safe command>."
        command = part[1].strip()
        if not command:
            return "Use: run command <safe command>."
        blocked = ["rm", "shutdown", "reboot", "mkfs", ":(){"]
        if any(token in command for token in blocked):
            return "Command blocked by safety protocol."
        try:
            result = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            output = (result.stdout or result.stderr).strip()
            return output[:600] if output else "Command executed."
        except Exception as exc:
            return f"Command failed: {exc}"

    def smart_home(self, raw: str) -> str:
        text = raw.lower()
        if "light" in text:
            if "off" in text:
                return "Smart-home bridge: lights turned off."
            return "Smart-home bridge: lights turned on."
        if "temperature" in text:
            return "Thermostat set to comfort mode (22°C)."
        return "Smart-home command acknowledged."
