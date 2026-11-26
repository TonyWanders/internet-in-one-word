#!/usr/bin/env python3
"""One word for the whole internet, written to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The word is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 30 characters, a single word, not only white space.
The file holds exactly the word, nothing else, no trailing newline.
"""

import os
import sys
from pathlib import Path

CHOSEN = "feral"

LOW = 1
HIGH = 30
FALLBACK = "/output/entry.txt"


def pick_target() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(FALLBACK)


class WordEntry:
    """A single-word entry with its competition gate and output target."""

    def __init__(self, text: str) -> None:
        self.text = text

    def check(self) -> int:
        """Enforce the gate: 1 to 30 chars, one word, not blank.

        Returns the character count. Raises ValueError when the gate fails.
        """
        count = len(self.text)
        if not (LOW <= count <= HIGH):
            raise ValueError(f"word is {count} characters, outside 1-30")
        if not self.text.strip():
            raise ValueError("word is only white space")
        if len(self.text.split()) != 1:
            raise ValueError("entry must be a single word")
        return count

    def destination(self) -> Path:
        return pick_target()

    def save(self) -> int:
        """Validate, write the word, and report its character count."""
        count = self.check()
        target = self.destination()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.text, encoding="utf-8")
        print(f"wrote {count} characters to {target}")
        return 0


def run() -> int:
    try:
        return WordEntry(CHOSEN).save()
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
