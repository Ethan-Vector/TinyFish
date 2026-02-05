from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List

from .base import FinalAction, ToolAction, Action


@dataclass
class DummyProvider:
    """Deterministic provider for tests and smoke runs.

    Rules:
    - If the last user message looks like math, call calc.
    - If it contains 'write note:' call note_append.
    - Else: final echo summary.
    """

    name: str = "dummy"

    def next_action(self, *, system: str, messages: List[Dict[str, str]]) -> Action:
        last = messages[-1]["content"] if messages else ""
        text = last.strip()

        m = re.search(r"write note\s*:\s*(.+)$", text, re.IGNORECASE)
        if m:
            return ToolAction(type="tool", name="note_append", args={"line": m.group(1).strip()})

        # Very naive math detection for demos.
        if re.fullmatch(r"[0-9\s\+\-\*\/\(\)\.]+", text) and any(ch.isdigit() for ch in text):
            return ToolAction(type="tool", name="calc", args={"expr": text})

        # If the user asks to read notes
        if re.search(r"read\s+notes", text, re.IGNORECASE):
            return ToolAction(type="tool", name="read_file", args={"path": "notes.txt"})

        return FinalAction(type="final", content=f"I can help. Try math like '19*7' or 'write note: ...'. You said: {text}")
