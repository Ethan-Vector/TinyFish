from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Protocol


class Tool(Protocol):
    name: str
    description: str

    def __call__(self, **kwargs: Any) -> str: ...


@dataclass
class ToolError(Exception):
    message: str

    def __str__(self) -> str:
        return self.message
