# Production-Ready Skeleton (Python/FastAPI)

This folder provides a clean starting architecture with:
- explicit app factory (`create_app`) for testability,
- isolated server startup module,
- a health endpoint,
- unit tests,
- CI hooks via repository workflow.

## Local setup

```bash
cd production-skeleton
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
python src/server.py
```
