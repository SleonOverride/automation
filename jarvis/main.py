from __future__ import annotations

import argparse

from jarvis.assistant import JarvisAssistant
from jarvis.config import JarvisConfig
from jarvis.io import TextIO, VoiceIO


def main() -> None:
    parser = argparse.ArgumentParser(description="Jarvis-inspired Python assistant")
    parser.add_argument("--voice", action="store_true", help="Enable microphone and TTS mode")
    args = parser.parse_args()

    cfg = JarvisConfig.from_env()
    use_voice = args.voice or cfg.enable_voice
    io_backend = VoiceIO() if use_voice else TextIO()

    assistant = JarvisAssistant(cfg=cfg, io_backend=io_backend)
    assistant.run()


if __name__ == "__main__":
    main()
