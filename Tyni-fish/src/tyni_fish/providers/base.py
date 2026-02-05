from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Protocol


@dataclass(frozen=True)
class ToolAction:
    type: str
    name: str
    args: Dict[str, Any]


@dataclass(frozen=True)
class FinalAction:
    type: str
    content: str


Action = ToolAction | FinalAction


class Provider(Protocol):
    name: str

    def next_action(self, *, system: str, messages: List[Dict[str, str]]) -> Action: ...
