from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Set


@dataclass(frozen=True)
class Policy:
    """Guardrails for the agent runtime.

    Keep this small and enforceable. You can add more later (token budgets, etc.).
    """

    max_steps: int = 8
    tool_timeout_secs: int = 5
    allow_tools: Set[str] = field(default_factory=lambda: {"calc", "note_append", "read_file", "write_file", "echo"})

    def with_overrides(self, *, max_steps: int | None = None) -> "Policy":
        return Policy(
            max_steps=max_steps if max_steps is not None else self.max_steps,
            tool_timeout_secs=self.tool_timeout_secs,
            allow_tools=set(self.allow_tools),
        )

    @staticmethod
    def from_env() -> "Policy":
        import os

        max_steps = int(os.getenv("TYNI_MAX_STEPS", "8"))
        tool_timeout = int(os.getenv("TYNI_TOOL_TIMEOUT_SECS", "5"))
        return Policy(max_steps=max_steps, tool_timeout_secs=tool_timeout)
