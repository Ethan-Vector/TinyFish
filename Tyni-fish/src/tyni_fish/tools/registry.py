from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping

from .base import Tool, ToolError


@dataclass
class ToolRegistry:
    tools: Dict[str, Tool] = field(default_factory=dict)

    def register(self, tool: Tool) -> None:
        if not getattr(tool, "name", None):
            raise ToolError("Tool must have a non-empty 'name'.")
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self.tools:
            raise ToolError(f"Unknown tool: {name}")
        return self.tools[name]

    def list(self) -> Dict[str, str]:
        return {name: getattr(tool, "description", "") for name, tool in self.tools.items()}
