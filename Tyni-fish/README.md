# Tyni Fish

**Tyni Fish** is a *budget-first* agent template you can actually ship: a lightweight agent loop, a strict tool allowlist, timeouts, trace logs, and a tiny eval harness.

It’s intentionally small: if you can’t operate it, you can’t ship it.

---

## What you get

- **Agent loop** with explicit `tool` / `final` actions
- **Tool registry** + built-in safe tools (calc, note, read/write in `workspace/`)
- **Guardrails**: allowlist, max steps, per-tool timeout, path sandbox
- **Tracing**: JSONL traces per run (`traces/`)
- **Evals**: `evals/datasets/smoke.jsonl` + harness
- **CI**: Ruff + Pytest + smoke evals
- **Docker**: container-ready

---

## Quickstart

### 1) Local (recommended)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m tyni_fish.evals.harness
tyni-fish run --input "What is 19 * 7?"
```

### 2) Interactive chat
```bash
tyni-fish chat
```

---

## Providers (LLM backends)

- `dummy` (default): deterministic behavior for tests and smoke runs
- `openai-compat`: OpenAI-compatible Chat Completions endpoint (self-hosted or cloud)

Example:
```bash
export OPENAI_API_KEY="..."
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4o-mini"
tyni-fish run --provider openai-compat --input "Draft a plan to..."
```

> Note: this repo avoids heavyweight dependencies by design. If you want richer schemas, add Pydantic/JSONSchema later.

---

## Project layout

- `src/tyni_fish/` core library + CLI
- `workspace/` sandboxed filesystem for tools
- `evals/` datasets (JSONL)
- `docs/` practical guides

---

## Why “Tyni Fish”?

Because in production, your “agent” should behave like a *small fish*:
- fast,
- cheap,
- predictable,
- and never bites your hand.

---

## License

MIT — see `LICENSE`.
