# Adding Tools

## 1) Implement the tool

Create a class that implements `Tool` (see `src/tyni_fish/tools/base.py`).

Key rules:
- Validate inputs (types, ranges).
- Respect the workspace sandbox.
- Never exfiltrate secrets.
- Keep runtime bounded.

## 2) Register it

Add it to the registry in `src/tyni_fish/tools/builtins.py`.

## 3) Allowlist it

Update `configs/tyni_fish.json` and/or set policy in code to include the tool name.

## 4) Add tests + evals

- Unit test: correct output + failure modes
- Eval: one JSONL case proving end-to-end behavior

Tip: if a tool is expensive or flaky, wrap it with a stub and test the stub in CI.
