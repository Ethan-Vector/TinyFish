from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, Optional

from ..agent import AgentRunner


@dataclass
class Case:
    id: str
    input: str
    expected_contains: List[str]
    max_steps: Optional[int] = None


def _load_cases(path: str) -> List[Case]:
    cases: List[Case] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            cases.append(
                Case(
                    id=str(obj["id"]),
                    input=str(obj["input"]),
                    expected_contains=list(obj.get("expected_contains", [])),
                    max_steps=obj.get("max_steps"),
                )
            )
    return cases


def run_dataset(path: str, *, provider_name: str = "dummy") -> bool:
    runner = AgentRunner.from_config(provider_name=provider_name)
    total = 0
    passed = 0

    for case in _load_cases(path):
        total += 1
        try:
            out = runner.run(case.input, max_steps=case.max_steps)
            ok = all(s in out for s in case.expected_contains)
        except Exception as e:
            out = f"ERROR: {e}"
            ok = False

        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {case.id}")
        if not ok:
            print("  output:", out)
            print("  expected_contains:", case.expected_contains)
        else:
            passed += 1

    print(f"Result: {passed}/{total} passed")
    return passed == total


def main() -> None:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="evals/datasets/smoke.jsonl")
    p.add_argument("--provider", default="dummy")
    args = p.parse_args()

    ok = run_dataset(args.dataset, provider_name=args.provider)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
