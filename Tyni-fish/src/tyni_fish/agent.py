from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .policy import Policy
from .tracing import TraceWriter
from .providers.base import Action, FinalAction, Provider, ToolAction
from .providers.dummy import DummyProvider
from .providers.openai_compat import OpenAICompatProvider
from .tools.base import ToolError
from .tools.builtins import default_registry
from .tools.registry import ToolRegistry


SYSTEM_PROMPT = """You are an agent that must output a single JSON object representing the next action.

Allowed action shapes:
1) Tool call:
  {"type":"tool","name":"<tool_name>","args":{...}}
2) Final answer:
  {"type":"final","content":"..."} 

Rules:
- Use tools only when needed.
- If you use a tool, be explicit and minimal in args.
- Never invent tool results.
- If you can answer directly, return type=final.
"""


def _run_with_timeout(fn, timeout_secs: int):
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(fn)
        return fut.result(timeout=timeout_secs)


@dataclass
class AgentRunner:
    policy: Policy
    tools: ToolRegistry
    provider: Provider
    workspace_dir: str = "workspace"
    trace_dir: str = "traces"
    tracing: bool = True

    @staticmethod
    def from_config(
        *,
        provider_name: str = "dummy",
        policy: Optional[Policy] = None,
        workspace_dir: str = "workspace",
        trace_dir: str = "traces",
    ) -> "AgentRunner":
        policy = policy or Policy.from_env()
        tools = default_registry(workspace_dir=workspace_dir)
        provider = _make_provider(provider_name)
        return AgentRunner(policy=policy, tools=tools, provider=provider, workspace_dir=workspace_dir, trace_dir=trace_dir)

    def run(self, user_input: str, *, max_steps: Optional[int] = None) -> str:
        os.makedirs(self.workspace_dir, exist_ok=True)

        policy = self.policy.with_overrides(max_steps=max_steps) if max_steps is not None else self.policy
        trace = TraceWriter(trace_dir=self.trace_dir) if self.tracing else None

        messages: List[Dict[str, str]] = [{"role": "user", "content": user_input}]
        if trace:
            trace.write({"event": "start", "provider": getattr(self.provider, "name", "unknown"), "policy": policy.__dict__})

        for step in range(policy.max_steps):
            action = self.provider.next_action(system=SYSTEM_PROMPT, messages=messages)
            if trace:
                trace.write({"event": "action", "step": step, "action": _action_to_dict(action)})

            if isinstance(action, FinalAction):
                if trace:
                    trace.write({"event": "final", "step": step})
                return action.content

            if isinstance(action, ToolAction):
                if action.name not in policy.allow_tools:
                    raise RuntimeError(f"Tool not allowed by policy: {action.name}")
                tool = self.tools.get(action.name)

                def call():
                    return tool(**(action.args or {}))

                try:
                    result = _run_with_timeout(call, policy.tool_timeout_secs)
                except Exception as e:
                    result = f"TOOL_ERROR: {e}"

                if trace:
                    trace.write({"event": "tool_result", "step": step, "tool": action.name, "result": result})

                messages.append({"role": "assistant", "content": json.dumps(_action_to_dict(action))})
                messages.append({"role": "tool", "content": result})
                continue

            raise RuntimeError(f"Unknown action type: {action}")

        raise RuntimeError("Max steps exceeded")


def _action_to_dict(action: Action) -> Dict[str, Any]:
    if isinstance(action, ToolAction):
        return {"type": "tool", "name": action.name, "args": action.args}
    return {"type": "final", "content": action.content}


def _make_provider(provider_name: str) -> Provider:
    name = provider_name.strip().lower()
    if name in {"dummy", "test"}:
        return DummyProvider()
    if name in {"openai", "openai-compat", "oai"}:
        return OpenAICompatProvider()
    raise ValueError(f"Unknown provider: {provider_name}")
