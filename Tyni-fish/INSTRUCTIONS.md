# INSTRUCTIONS

This repo is meant to be **cloned and adapted**. Here’s the workflow I recommend.

## 1) Decide your contract
Pick one primary user-facing contract and keep it stable:
- CLI (`tyni-fish run ...`)
- HTTP API (add later)
- Library API (already present via `AgentRunner`)

## 2) Add tools *safely*
- Add a tool class in `src/tyni_fish/tools/`
- Register it in `tools/builtins.py` (or a new module)
- Update allowlist / policy if needed
- Write 1 unit test + 1 eval case

See `docs/ADDING_TOOLS.md`.

## 3) Tighten guardrails first
Start strict and loosen only when you have evidence:
- Keep a small tool allowlist
- Keep step budgets low
- Enforce sandboxed paths
- Trace every run

## 4) Evals are your “release gate”
Add at least:
- 5 smoke cases (cheap)
- 20 regression cases (stable)
- 5 adversarial cases (nasty)

See `docs/EVALS.md`.

## 5) Productionization checklist (minimum)
- add structured logging + trace IDs
- add retries around the provider (idempotent)
- add rate limits + circuit breakers
- ship dashboards: p95 latency, tool error rate, pass@k eval trend

If you want a more complete “platform” structure, you can split:
- runner
- tool server
- eval service
- orchestration

But don’t start there.
