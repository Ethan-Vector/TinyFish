# Evals

Evals are deliberately tiny here: they’re a *release gate*, not a research project.

## Dataset format

`evals/datasets/*.jsonl` with one JSON object per line.

Fields used by the harness:
- `id`: string
- `input`: string
- `expected_contains`: list of substrings that must appear in the final output
- `max_steps` (optional): override policy per case

## Run

```bash
python -m tyni_fish.evals.harness
```

The harness exits non-zero if any case fails.

## Extending

If you want richer scoring:
- exact match
- regex expectations
- tool call expectations
- structured outputs

Add fields and update `harness.py`.
