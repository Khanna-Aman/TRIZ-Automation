# Quickstart

1) Build & run
- make build && make up

2) Verify
- curl http://localhost:8000/health
- curl -X POST http://localhost:8000/problems/start -H 'Content-Type: application/json' -d '{"problem_statement":"Reduce drone weight"}'

3) n8n
- Open http://localhost:5678 and import the workflow from 05-Workflows.md

4) TRIZ data (optional)
- make import-triz

