# CONTRIBUTING

## Dev setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

## Pull requests
- Keep changes focused
- Add tests for behavior changes
- Add at least one eval case for new tool or policy change
- Update docs if you change CLI flags
