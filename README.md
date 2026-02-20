# Jarvis (Python)

A feature-rich, **Jarvis-inspired** assistant you can run locally from terminal (text mode) or microphone/speaker (voice mode).

## Features

- Conversational command loop (text + optional voice)
- Time/date/weather queries
- Personal memory core (`remember ...`, `recall`)
- Reminder system (`remind me ...`, `list reminders`)
- Safe shell command execution (`run command ...`)
- Web search launcher
- App shortcuts (`open github`, `open youtube`, etc.)
- Security protocol simulation (`arm security`, `disarm security`)
- Smart-home simulation (`lights on/off`, `set temperature`)
- Persistent JSON state files

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
jarvis
```

## Voice mode (optional)

```bash
pip install -e ".[voice]"
jarvis --voice
```

## Example commands

- `help`
- `what time is it`
- `weather`
- `remember the arc reactor needs maintenance`
- `recall`
- `remind me to check the suit diagnostics at 8pm`
- `list reminders`
- `open github`
- `search nanotech suit design`
- `run command python --version`
- `arm security`
- `lights off`
- `shutdown`

## Environment variables

- `JARVIS_OWNER` (default: `Boss`)
- `JARVIS_WAKE_WORD` (reserved for future wake-word support)
- `JARVIS_WEATHER_LOCATION` (example: `New York`)
- `JARVIS_MEMORY_FILE`
- `JARVIS_REMINDERS_FILE`
- `JARVIS_LOG_FILE`
- `JARVIS_ENABLE_VOICE=true`

## Notes

This project aims to deliver a practical, extensible Jarvis-like assistant with many high-value capabilities. Movie-only features such as autonomous flight control, physical suit integration, and cinematic holograms are represented as software simulations/hooks in this version.
