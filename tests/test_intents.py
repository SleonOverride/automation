from jarvis.intents import parse_intent


def test_shutdown_intent():
    assert parse_intent("please shutdown now").name == "shutdown"


def test_reminder_intent():
    assert parse_intent("remind me to run diagnostics").name == "reminder"


def test_general_intent():
    assert parse_intent("tell me a joke").name == "general"
