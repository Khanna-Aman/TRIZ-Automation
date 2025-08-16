# Testing Strategy

## Levels
- Unit tests for service logic (parsers, scorers)
- API tests for endpoints (health, happy path, error cases)
- Integration tests with test containers (Postgres, Qdrant, Neo4j)

## Coverage Targets (initial)
- 60% across services in MVP; increase as logic grows

## Running
- Locally: `pytest -q`
- CI: see .github/workflows/ci.yml

## Data
- Use minimal fixtures; for TRIZ, seed a small subset for tests

