from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


@dataclass
class TraceWriter:
    trace_dir: str = "traces"
    run_id: str = ""

    def __post_init__(self) -> None:
        if not self.run_id:
            self.run_id = uuid.uuid4().hex
        os.makedirs(self.trace_dir, exist_ok=True)
        self.path = os.path.join(self.trace_dir, f"{self.run_id}.jsonl")

    def write(self, event: Dict[str, Any]) -> None:
        event = dict(event)
        event.setdefault("ts", time.time())
        event.setdefault("run_id", self.run_id)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
