## Intuitive Inventive Agent (IIA) — Dev Scaffold

This repository contains a minimal, runnable scaffold for the IIA system described in the concept and architecture docs. It includes:
- Docker Compose stack for core services and infra
- FastAPI service stubs (orchestrator, triz, lateral, rag, eval, worker)
- n8n and LangGraph MVP workflows (see 05-Workflows.md)

Use this to iterate quickly and replace stubs with real logic.

---

### Prerequisites
- Docker Desktop (or Docker Engine) + Docker Compose v2
- Optional (for local scripts): Python 3.11+

---

### Compose files
- Primary compose: 11-02-docker-compose.yml (use this one)
- A second scaffold also exists at docker-compose.yml; prefer the 11-02 file to avoid duplication

Bring the stack up:
- docker compose -f 11-02-docker-compose.yml build
- docker compose -f 11-02-docker-compose.yml up -d

Shutdown:
- docker compose -f 11-02-docker-compose.yml down

---

### Services
- Orchestrator (FastAPI + LangGraph placeholder): http://localhost:8000
- TRIZ (FastAPI): internal at http://triz:8000
- Lateral (FastAPI): internal at http://lateral:8000
- RAG-Graph (FastAPI): internal at http://rag:8000
- Evaluation & Evolution (FastAPI): internal at http://eval:8000
- Worker (placeholder FastAPI): internal at http://worker:8000
- Postgres: localhost:5432 (user: iia, pass: iia, db: iia)
- Redis: localhost:6379
- RabbitMQ: localhost:5672 (management UI: http://localhost:15672)
- Qdrant: http://localhost:6333
- Neo4j: http://localhost:7474 (Bolt: 7687; auth neo4j/password)
- MinIO: http://localhost:9000 (console: http://localhost:9001, admin/adminadmin)
- n8n: http://localhost:5678

Health checks (examples):
- curl http://localhost:8000/health  # orchestrator
- Inside network (via another container) you can hit /health on triz/lateral/rag/eval

---

### Minimal API usage
Start a run (stubbed):
- curl -X POST http://localhost:8000/problems/start -H "Content-Type: application/json" -d '{"problem_statement":"Reduce drone weight","context":"materials"}'

TRIZ (internal):
- POST triz:8000/triz/resolve {"problem":"..."}

Lateral (internal):
- POST lateral:8000/lateral/generate {"problem":"..."}

---

### TRIZ data import (schema + sample)
Schema and script:
- services/triz/schema.sql
- services/triz/import_triz_matrix.py
- Sample data: services/triz/sample/{principles.json, parameters.json, matrix.csv}

Run locally (preferred):
1) Ensure Postgres is up from Compose
2) pip install psycopg[binary]
3) set POSTGRES_URL=postgresql://iia:iia@localhost:5432/iia
4) python services/triz/import_triz_matrix.py --principles services/triz/sample/principles.json --parameters services/triz/sample/parameters.json --matrix services/triz/sample/matrix.csv

Notes:
- Replace the sample files with the full 40 principles, 39 parameters, and the complete 39×39 mapping.
- You can re-run the import; it upserts principles/parameters and deduplicates matrix links.

---

### n8n MVP workflow
- See 05-Workflows.md for an importable JSON workflow that:
  - Receives a Webhook → (optional) RAG ingest → TRIZ → Lateral → Merge → Evaluate → Respond
- Steps:
  1) Visit http://localhost:5678, create a new workflow
  2) Import the JSON block (MVP-Orchestration-SinglePass)
  3) Open Webhook node and copy the Test URL
  4) POST a payload like: {"problem":"Reduce drone weight","url":"https://example.com"}

---

### LangGraph MVP
- 05-Workflows.md includes a minimal graph definition with async httpx calls
- To run: create a small runner that calls app.ainvoke({"problem":"..."})

---

### Development tips
Logs:
- docker compose -f 11-02-docker-compose.yml logs -f orchestrator
- docker compose -f 11-02-docker-compose.yml ps

Exec into a container:
- docker exec -it iia-orchestrator /bin/sh

Rebuild a single service:
- docker compose -f 11-02-docker-compose.yml build orchestrator && docker compose -f 11-02-docker-compose.yml up -d orchestrator

---

### Next steps
- Wire orchestrator to actually call TRIZ/Lateral/RAG/Eval services and persist runs in Postgres
- Add per-service requirements.txt/poetry and pin versions
- Introduce basic tests (pytest) and GitHub Actions CI
- Add API gateway (Traefik/Kong) and Keycloak SSO when ready
- Add observability (OTel SDKs, Prometheus, Grafana, Loki) per 02_Tech_Stack.md

