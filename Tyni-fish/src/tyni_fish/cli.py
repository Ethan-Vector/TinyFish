from __future__ import annotations

import argparse
import json
import os
import sys

from .agent import AgentRunner
from .policy import Policy


def main() -> None:
    parser = argparse.ArgumentParser(prog="tyni-fish", description="Tyni Fish agent template.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Run one-shot input through the agent.")
    p_run.add_argument("--input", required=True, help="User input string.")
    p_run.add_argument("--provider", default=os.getenv("TYNI_PROVIDER", "dummy"), help="Provider: dummy|openai-compat")
    p_run.add_argument("--max-steps", type=int, default=None, help="Override max steps for this run.")
    p_run.add_argument("--no-trace", action="store_true", help="Disable tracing.")

    p_chat = sub.add_parser("chat", help="Interactive chat (single-turn loop).")
    p_chat.add_argument("--provider", default=os.getenv("TYNI_PROVIDER", "dummy"), help="Provider: dummy|openai-compat")
    p_chat.add_argument("--no-trace", action="store_true", help="Disable tracing.")

    p_evals = sub.add_parser("evals", help="Run smoke evals.")
    p_evals.add_argument("--dataset", default="evals/datasets/smoke.jsonl", help="Path to JSONL dataset.")
    p_evals.add_argument("--provider", default="dummy", help="Provider for evals (default dummy).")

    args = parser.parse_args()

    if args.cmd == "run":
        runner = AgentRunner.from_config(provider_name=args.provider)
        runner.tracing = not args.no_trace
        out = runner.run(args.input, max_steps=args.max_steps)
        print(out)
        return

    if args.cmd == "chat":
        runner = AgentRunner.from_config(provider_name=args.provider)
        runner.tracing = not args.no_trace
        print("Tyni Fish chat. Type 'exit' to quit.")
        while True:
            try:
                line = input("> ").strip()
            except EOFError:
                break
            if not line:
                continue
            if line.lower() in {"exit", "quit"}:
                break
            try:
                out = runner.run(line)
            except Exception as e:
                out = f"ERROR: {e}"
            print(out)
        return

    if args.cmd == "evals":
        from .evals.harness import run_dataset

        ok = run_dataset(args.dataset, provider_name=args.provider)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
