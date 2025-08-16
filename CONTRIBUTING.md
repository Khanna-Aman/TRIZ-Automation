## Contributing Guide

Thank you for contributing to the Intuitive Inventive Agent (IIA) project! This guide explains how to set up your environment, run services, test, and follow style conventions.

### Getting Started
- Install Docker Desktop and Make
- Build and run: `make build && make up`
- Orchestrator health: `curl http://localhost:8000/health`

### Development
- Use Python 3.11+
- Create a virtualenv and install tooling for local work:
  - `pip install -U pip pytest ruff black isort mypy`
- Pre-commit hooks (optional):
  - `pip install pre-commit && pre-commit install`

### Tests
- Add tests under `tests/<service>/` with `test_*.py` naming
- Run locally: `pytest -q`

### Style & Lint
- Formatting: `black .`
- Imports: `isort .`
- Lint: `ruff .`
- Types: `mypy services/`

### Commit Messages
- Use concise, present-tense summary (50 chars) + details as needed
- Reference issues where applicable

### Pull Requests
- Include description, screenshots/logs when relevant
- Ensure CI passes (tests, lint, type checks)

### Security
- Do not commit secrets. Use `.env` or secret managers
- Report vulnerabilities via SECURITY.md

