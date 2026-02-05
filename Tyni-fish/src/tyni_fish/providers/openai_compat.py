from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List

from .base import Action, FinalAction, ToolAction


def _env(name: str, default: str = "") -> str:
    v = os.getenv(name)
    return v if v is not None and v != "" else default


@dataclass
class OpenAICompatProvider:
    """OpenAI-compatible Chat Completions provider.

    This implementation is intentionally dependency-free (urllib).
    Endpoint must support:
      POST {base_url}/chat/completions
    and return a standard OpenAI response.

    NOTE: This repo doesn't ship prompts that guarantee tool-calling.
    Use it as a starting point and tune the system prompt for your model.
    """

    name: str = "openai-compat"
    base_url: str = ""
    api_key: str = ""
    model: str = ""

    def __post_init__(self) -> None:
        self.base_url = self.base_url or _env("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.api_key = self.api_key or _env("OPENAI_API_KEY", "")
        self.model = self.model or _env("OPENAI_MODEL", "gpt-4o-mini")

    def next_action(self, *, system: str, messages: List[Dict[str, str]]) -> Action:
        url = self.base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}] + messages,
            "temperature": 0.2,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")

        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")

        obj = json.loads(raw)
        content = obj["choices"][0]["message"].get("content", "")

        # Expect JSON action in content (tool/final).
        try:
            action = json.loads(content)
        except Exception:
            return FinalAction(type="final", content=content)

        if action.get("type") == "tool":
            return ToolAction(type="tool", name=action.get("name", ""), args=action.get("args", {}) or {})
        return FinalAction(type="final", content=action.get("content", content))
