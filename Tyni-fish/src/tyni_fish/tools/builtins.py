from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Any

from .base import ToolError
from .registry import ToolRegistry


def _safe_workspace_path(workspace_dir: str, path: str) -> str:
    # Prevent path traversal: all operations must stay under workspace_dir.
    workspace_dir = os.path.abspath(workspace_dir)
    target = os.path.abspath(os.path.join(workspace_dir, path))
    if not target.startswith(workspace_dir + os.sep) and target != workspace_dir:
        raise ToolError("Path is outside workspace sandbox.")
    return target


@dataclass
class CalcTool:
    name: str = "calc"
    description: str = "Evaluate a simple arithmetic expression (digits and + - * / ( ) .)."

    def __call__(self, **kwargs: Any) -> str:
        expr = str(kwargs.get("expr", "")).strip()
        if not expr:
            raise ToolError("calc: missing 'expr'")
        # Very strict allowlist to avoid code execution.
        allowed = set("0123456789+-*/(). %")
        if any(ch not in allowed for ch in expr):
            raise ToolError("calc: invalid characters in expression.")
        # Safe eval in restricted namespace.
        try:
            value = eval(expr, {"__builtins__": {}}, {"math": math})
        except Exception as e:
            raise ToolError(f"calc: error: {e}")
        return str(value)


@dataclass
class EchoTool:
    name: str = "echo"
    description: str = "Echo back a message."

    def __call__(self, **kwargs: Any) -> str:
        return str(kwargs.get("text", ""))


@dataclass
class NoteAppendTool:
    workspace_dir: str
    name: str = "note_append"
    description: str = "Append a line to workspace/notes.txt."

    def __call__(self, **kwargs: Any) -> str:
        line = str(kwargs.get("line", "")).rstrip("\n")
        if not line:
            raise ToolError("note_append: missing 'line'")
        path = _safe_workspace_path(self.workspace_dir, "notes.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return "ok"


@dataclass
class ReadFileTool:
    workspace_dir: str
    name: str = "read_file"
    description: str = "Read a text file from workspace/."

    def __call__(self, **kwargs: Any) -> str:
        rel = str(kwargs.get("path", "")).strip()
        if not rel:
            raise ToolError("read_file: missing 'path'")
        path = _safe_workspace_path(self.workspace_dir, rel)
        if not os.path.exists(path):
            raise ToolError("read_file: file not found")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()


@dataclass
class WriteFileTool:
    workspace_dir: str
    name: str = "write_file"
    description: str = "Write a text file to workspace/ (overwrites)."

    def __call__(self, **kwargs: Any) -> str:
        rel = str(kwargs.get("path", "")).strip()
        content = str(kwargs.get("content", ""))
        if not rel:
            raise ToolError("write_file: missing 'path'")
        path = _safe_workspace_path(self.workspace_dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return "ok"


def default_registry(*, workspace_dir: str = "workspace") -> ToolRegistry:
    reg = ToolRegistry()
    reg.register(CalcTool())
    reg.register(EchoTool())
    reg.register(NoteAppendTool(workspace_dir=workspace_dir))
    reg.register(ReadFileTool(workspace_dir=workspace_dir))
    reg.register(WriteFileTool(workspace_dir=workspace_dir))
    return reg
