# Architecture

Tyni Fish is intentionally simple:

1. **Provider** returns an action:
   - `{"type": "tool", "name": "...", "args": {...}}`
   - `{"type": "final", "content": "..."}`

2. **AgentRunner** enforces policy:
   - tool allowlist
   - max steps
   - per-tool timeout

3. **Tools** run in a sandboxed workspace:
   - only `workspace/` is writable/readable by default

4. **Tracing** is always-on by default:
   - one JSONL file per run in `traces/`

## Data flow (high level)

User input → Provider → Action
- If tool: execute tool → append observation → next step
- If final: return content

That’s it. No magic.
